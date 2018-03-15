"""Implements a journal of games"""

import pickle
from typing import BinaryIO, List, Dict
from vtes.game import Game, Player

class Ranking:
    """Represents a ranking of a player in a game series"""
    # pylint: disable=too-few-public-methods
    def __init__(self, name: str, wins: int, points: float, games: int) -> None:
        self.player: str = name
        self.wins: int = wins
        self.points: float = points
        self.games: int = games
        self.total_possible_vp: int = 0

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
        if not self.total_possible_vp:
            return None

        return round(float(self.points)/float(self.total_possible_vp)*100)

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
        rankings[player.name].total_possible_vp += player_count

    def __init__(self) -> None:
        self.games: List[Game] = []

    def __iter__(self):
        yield from self.games

    def __len__(self) -> int:
        return len(self.games)

    def add(self, game: Game) -> None:
        """Add a Game to the journal"""
        self.games.append(game)

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

def load_store(storage: BinaryIO) -> GameStore:
    """Create a GameStore from storage"""
    return pickle.load(storage)
