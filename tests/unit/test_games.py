# I do not have that high criteria for test code
# pylint: disable=missing-docstring
from vtes.game import Game

def test_game():
    table = ("P1", "P2", "P3", "P4", "P5")
    game = Game(table)
    assert game.table == table