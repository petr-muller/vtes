"""Implements a journal of games"""

import pickle
from typing import BinaryIO, List
from vtes.game import Game

class GameStore:
    """Implements a journal of games"""
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

def load_store(storage: BinaryIO) -> GameStore:
    """Create a GameStore from storage"""
    return pickle.load(storage)
