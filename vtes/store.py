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
        yield from (self.player, self.wins, self.points, self.games)

class GameStore:
    """Implements a journal of games"""
    @staticmethod
    def _include_player_in_rankings(rankings: Dict[str, Ranking],
                                    player: Player, game: Game) -> None:
        """Include results of `player` in `game` into `rankings`"""
        if player.name not in rankings:
            rankings[player.name] = Ranking(player.name, 0, 0, 0)
        rankings[player.name].games += 1
        if player.points is not None:
            rankings[player.name].points += player.points
        if player.name == game.winner:
            rankings[player.name].wins += 1

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
        pickle.dump(self, storage)

    def rankings(self) -> List[Ranking]:
        """Return a list of player rankings, sorted by GW, then VP, then games"""
        rankings: Dict[str, Ranking] = {}
        for game in self.games:
            for player in game.player_results:
                GameStore._include_player_in_rankings(rankings, player, game)

        return sorted(list(rankings.values()), reverse=True)

def load_store(storage: BinaryIO) -> GameStore:
    """Create a GameStore from storage"""
    return pickle.load(storage)
