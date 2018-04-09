"""Implements a journal of games"""

import pickle
from typing import BinaryIO, List, Dict, Tuple
from vtes.game import Game, Player

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

    def save(self, storage: BinaryIO) -> None:
        """Save the journal to the bytes file-like object"""
        pickle.dump(self, storage, protocol=pickle.HIGHEST_PROTOCOL)

    def rankings(self) -> List[Ranking]:
        """Return a list of player rankings, sorted by GW, then VP, then games"""
        rankings: Dict[str, Ranking] = {}
        for game in self.games:
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

    def decks(self, player: str) -> List[DeckRanking]:
        """Return a list of deck rankings, sorted by GW, then VP, then games"""
        decks: Dict[Tuple[str, str], DeckRanking] = {}
        for game in self.games:
            for game_player in game.player_results:
                if player is None or player == game_player.name:
                    GameStore._include_deck_in_rankings(decks, game_player.deck, game_player.name,
                                                        game_player.points,
                                                        len(game.player_results),
                                                        game_player.name == game.winner)

        return sorted(list(decks.values()), reverse=True)

def load_store(storage: BinaryIO) -> GameStore:
    """Create a GameStore from storage"""
    store = pickle.load(storage)

    # fill in missing attributes from possible old store
    for game in store:
        if not hasattr(game, "date"):
            setattr(game, "date", None)

    return store
