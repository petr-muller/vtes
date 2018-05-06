"""Implements a journal of games"""

import pickle
import pathlib
from typing import Sequence, List, Dict, Tuple
from vtes.game import Game, Player
from vtes.db import DATABASE, DatabaseGameModel, DatabasePlayerModel, DatabaseNamespaceModel

class Ranking:
    """Represents a ranking of a player in a game series"""
    # pylint: disable=too-few-public-methods
    def __init__(self, name: str, wins: int, points: float, games: int) -> None:
        self.player: str = name
        self.wins: int = wins
        self.points: float = points
        self.games: int = games
        self.vp_total: int = 0

    def __eq__(self, other):
        return (self.player == other.player and
                self.wins == other.wins and
                self.points == other.points and
                self.games == other.games)

    def __lt__(self, other):
        return (self.wins, self.points, self.games) < (other.wins, other.points, other.games)

    def __str__(self):
        return f"{self.player} GW={self.wins} VP={self.points} games={self.games}"

    def __repr__(self):
        return f"{self.player} GW={self.wins} VP={self.points} games={self.games}"

    def __iter__(self):
        yield from (self.player, self.wins, self.points, self.games, f"{self.gw_ratio}%",
                    f"{self.vp_ratio}%")

    @property
    def gw_ratio(self) -> int:
        """Return a percentage (0-100) of games the player won"""
        return round(float(self.wins)/float(self.games)*100) if self.games else None

    @property
    def vp_ratio(self) -> int:
        """Return a percentage (0-100) of VPs the player got"""
        if not self.vp_total:
            return None

        return round(float(self.points)/float(self.vp_total)*100)

class DeckRanking:
    """Represents a ranking of a deck in a game series"""
    def __init__(self, deck: str, player: str, gw: int, games: int, vp: int,
                 vp_total: int) -> None:
        self.deck: str = deck
        self.player: str = player
        self.gw: int = gw
        self.games: int = games
        self.vp: int = vp
        self.vp_total: int = vp_total

    @property
    def gw_ratio(self) -> int:
        """Return a percentage (0-100) of GWs the deck won"""
        return round(float(self.gw)/float(self.games)*100)

    @property
    def vp_ratio(self) -> int:
        """Return a percentage (0-100) of VPs the deck won"""
        return round(float(self.vp)/float(self.vp_total)*100)

    def __lt__(self, other):
        return ((self.gw_ratio, self.vp_ratio, self.deck, self.player) <
                (other.gw_ratio, other.vp_ratio, self.deck, self.player))

    def __eq__(self, other):
        return ((self.deck, self.player, self.gw, self.games, self.vp, self.vp_total) ==
                (other.deck, other.player, other.gw, other.games, other.vp, other.vp_total))

    def __str__(self):
        return f"{self.deck}({self.player}) {self.gw}/{self.games} GW {self.vp}/{self.vp_total} VP"

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield from (self.deck, self.player, f"{self.gw}/{self.games} ({self.gw_ratio}%)",
                    f"{self.vp}/{self.vp_total} ({self.vp_ratio}%)")


class GameStore:
    """Implements a journal of games"""
    @staticmethod
    def _include_player_in_rankings(rankings: Dict[str, Ranking], player: Player,
                                    game: Game, player_count: int) -> None:
        """Include results of `player` in `game` into `rankings`"""
        if player.name not in rankings:
            rankings[player.name] = Ranking(player.name, 0, 0, 0)
        rankings[player.name].games += 1
        if player.points is not None:
            rankings[player.name].points += player.points
        if player.name == game.winner:
            rankings[player.name].wins += 1
        rankings[player.name].vp_total += player_count

    def __init__(self) -> None:
        self.games: List[Game] = []

    def __iter__(self):
        yield from self.games

    def __len__(self) -> int:
        return len(self.games)

    def add(self, game: Game) -> None:
        """Add a Game to the journal"""
        self.games.append(game)

    def fix(self, index: int, game: Game) -> None:
        """Fix a Game already in the journal"""
        self.games[index] = game

    def rankings(self, namespace: str = None) -> List[Ranking]:
        """Return a list of player rankings, sorted by GW, then VP, then games"""
        rankings: Dict[str, Ranking] = {}
        for game in self.games:
            if namespace and not game.in_namespace(namespace.split('/')):
                continue
            for player in game.player_results:
                GameStore._include_player_in_rankings(rankings, player, game,
                                                      len(game.player_results))

        return sorted(list(rankings.values()), reverse=True)

    @staticmethod
    def _include_deck_in_rankings(rankings: Dict[Tuple[str, str], DeckRanking], deck: str,
                                  name: str, vp: int, total_vp: int, winner: bool) -> None:
        if not deck:
            return

        deck_id = (deck, name)
        if deck_id not in rankings:
            rankings[deck_id] = DeckRanking(deck, name, 0, 0, 0, 0)
        rankings[deck_id].games += 1
        rankings[deck_id].vp_total += total_vp
        if vp:
            rankings[deck_id].vp += vp
        if winner:
            rankings[deck_id].gw += 1

    def decks(self, player: str = None, namespace: str = None) -> List[DeckRanking]:
        """Return a list of deck rankings, sorted by GW, then VP, then games"""
        decks: Dict[Tuple[str, str], DeckRanking] = {}
        for game in self.games:
            if namespace and not game.in_namespace(namespace.split('/')):
                continue
            for game_player in game.player_results:
                if player is None or player == game_player.name:
                    GameStore._include_deck_in_rankings(decks, game_player.deck, game_player.name,
                                                        game_player.points,
                                                        len(game.player_results),
                                                        game_player.name == game.winner)

        return sorted(list(decks.values()), reverse=True)


class PickleStore():
    """VtES Game Store backed by a pickle file"""
    def __init__(self, path: str) -> None:
        self.journal_path: pathlib.Path = pathlib.Path(path)
        self.store: GameStore = GameStore()

    def open(self) -> None:
        """Load the store from a pickle file"""
        with self.journal_path.open('rb') as journal_file:
            self.store = pickle.load(journal_file)

        # fill in missing attributes from possible old store
        for game in self.store:
            if not hasattr(game, "date"):
                setattr(game, "date", None)
            if not hasattr(game, "namespace"):
                setattr(game, "namespace", None)

    def save(self) -> None:
        """Save the store to a pickle file"""
        with self.journal_path.open('wb') as journal_file:
            pickle.dump(self.store, journal_file, pickle.HIGHEST_PROTOCOL)

    def add(self, game: Game) -> None:
        """Add a Game to the journal"""
        self.store.add(game)

    def fix(self, index: int, game: Game) -> None:
        """Fix a Game already in the journal"""
        self.store.fix(index, game)

    def rankings(self, namespace: str = None) -> Sequence[Ranking]:
        """Return a list of player rankings, sorted by GW, then VP, then games"""
        return self.store.rankings(namespace)

    def decks(self, player: str = None, namespace: str = None) -> Sequence[DeckRanking]:
        """Return a list of deck rankings, sorted by GW, then VP, then games"""
        return self.store.decks(player=player, namespace=namespace)

    @property
    def games(self) -> Sequence[Game]:
        """Return a sequence of games present in the store"""
        return list(self.store.games)

    def __len__(self) -> int:
        return len(self.store)

    def __iter__(self) -> Game:
        yield from self.store

    def filter(self, namespace: str = None) -> Sequence[Game]:
        """Return a list of Games filtered by given criteria"""
        if namespace:
            return [game for game in self.store.games if game.in_namespace(namespace.split('\n'))]

        return self.games

class DatabaseStore():
    """VtES Game Store backed by a database"""
    def __init__(self, path: str) -> None:
        self.journal_path: pathlib.Path = pathlib.Path(path)

    def open(self) -> None:
        """Connect to a database and ensure all tables exist"""
        DATABASE.init(str(self.journal_path))
        DATABASE.connect()
        DATABASE.create_tables([DatabaseGameModel, DatabasePlayerModel, DatabaseNamespaceModel])

    @staticmethod
    def add(game: Game) -> None:
        """Add a Game to the journal"""
        DatabaseGameModel.db_create(game)

    @staticmethod
    def save() -> None:
        """This is a NOP with database backend"""
        pass

    @staticmethod
    def rankings(namespace: str = None) -> Sequence[Ranking]:
        """Return a list of player rankings, sorter by GW, then VP, then games"""
        store = GameStore()
        store.games = DatabaseGameModel.all_games()
        return store.rankings(namespace)

    @staticmethod
    def decks(player: str = None, namespace: str = None) -> Sequence[DeckRanking]:
        """Return a list of deck rankings, sorted by GW, then VP, then games"""
        store = GameStore()
        store.games = DatabaseGameModel.all_games()
        return store.decks(player=player, namespace=namespace)

    def __len__(self) -> int:
        # Passing 'None' to avoid Pylint errors, WONTFIX in peewee
        # https://github.com/coleifer/peewee/issues/1466
        return DatabaseGameModel.select().count(None)

    def __iter__(self):
        yield from DatabaseGameModel.all_games()

    def filter(self, namespace: str = None):
        """Return a list of Games filtered by given criteria"""
        if namespace:
            yield from [game for game in list(self) if game.in_namespace(namespace.split('\n'))]
        else:
            yield from self
