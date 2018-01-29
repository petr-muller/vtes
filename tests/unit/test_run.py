# I do not have that high criteria for test code
# pylint: disable=missing-docstring, redefined-outer-name

from unittest.mock import Mock, MagicMock, patch
from io import BytesIO
import pathlib
import pytest

from vtes.run import ParsePlayerAction, games_command, add_command
from vtes.store import GameStore, load_store

from vtes.game import Game

@pytest.fixture
def store_with_two_games():
    store = GameStore()
    store.add(Game(("1", "2", "3", "4", "5")))
    store.add(Game(("A", "B", "C", "D", "E")))
    return store

def test_parse_players():
    action = ParsePlayerAction(dest="players", option_strings=("players", ))
    namespace = Mock()
    for valid_length in (3, 4, 5, 6):
        action(Mock(), namespace, ["x"] * valid_length)
        assert len(namespace.players) == valid_length

    for invalid_length in (0, 1, 2, 7, 8):
        with pytest.raises(ValueError):
            action(Mock(), namespace, ["x"] * invalid_length)

@patch('builtins.print')
def test_games_command(mock_print, store_with_two_games):
    with BytesIO() as fakefile:
        store_with_two_games.save(fakefile)
        fakefile.seek(0, 0)
        mock_path = MagicMock(pathlib.Path)
        mock_path.open.return_value = fakefile
        games_command(mock_path)

    assert mock_print.call_count == 2

def test_add_command_when_exists(store_with_two_games, fs):
    # pylint: disable=invalid-name, unused-argument
    fake_path = pathlib.Path("file")
    with fake_path.open("wb") as fakefile:
        store_with_two_games.save(fakefile)

    add_command(("1", "2", "3", "4", "5"), fake_path)
    add_command(("2", "3", "4", "5", "6"), fake_path)

    with fake_path.open("rb") as fakefile:
        new_store = load_store(fakefile)

    assert len(new_store) == 4

def test_add_command_when_not_exists(fs):
    # pylint: disable=invalid-name, unused-argument
    fake_path = pathlib.Path("file")

    add_command(("1", "2", "3", "4", "5"), fake_path)
    add_command(("2", "3", "4", "5", "6"), fake_path)

    with fake_path.open("rb") as fakefile:
        new_store = load_store(fakefile)

    assert len(new_store) == 2
