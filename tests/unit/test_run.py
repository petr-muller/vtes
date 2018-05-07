# I do not have that high criteria for test code
# pylint: disable=missing-docstring, redefined-outer-name

from unittest.mock import Mock, patch
import pytest
import dateutil.parser

from vtes.run import ParsePlayerAction, games_command, add_command, stats_command, gamefix_command
from vtes.store import PickleStore

from vtes.game import Game

@pytest.fixture
def store_with_two_games(fs): # pylint: disable=invalid-name, unused-argument
    store = PickleStore("file")
    store.add(Game.from_table(("1:3", "2:2", "3", "4", "5")))
    store.add(Game.from_table(("A:2", "B:1", "C:1", "D:1", "E")))
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
    store_with_two_games.save()

    games_command(store_with_two_games, namespace=None)
    assert mock_print.call_count == 2

@patch('builtins.print')
def test_stats_command(mock_print, store_with_two_games):
    store_with_two_games.save()

    stats_command(store_with_two_games, namespace=None)
    assert mock_print.call_count == 3

def test_add_command_when_exists(store_with_two_games, fs):
    # pylint: disable=invalid-name, unused-argument
    store_with_two_games.save()

    add_command(("1", "2", "3", "4", "5"), store_with_two_games, date=None, namespace=None)
    add_command(("2", "3", "4", "5", "6"), store_with_two_games, date=None, namespace=None)

    new_store = PickleStore("file")
    new_store.open()

    assert len(new_store) == 4

def test_add_command_when_not_exists(fs):
    # pylint: disable=invalid-name, unused-argument
    fake_journal = PickleStore("file")

    add_command(("1", "2", "3", "4", "5"), fake_journal, date=None, namespace=None)
    add_command(("2", "3", "4", "5", "6"), fake_journal, date=None, namespace=None)

    new_fake_journal = PickleStore("file")
    new_fake_journal.open()

    assert len(new_fake_journal) == 2

def test_gamefix_command(fs):
    # pylint: disable=invalid-name, unused-argument
    fake_journal = PickleStore("file")
    add_command(("1", "2", "3", "4", "5"), fake_journal, date=None, namespace=None)
    gamefix_command(0, fake_journal, ("A", "B", "C", "D", "E"), date=None, namespace=None)

    new_fake_journal = PickleStore("file")
    new_fake_journal.open()

    assert len(new_fake_journal) == 1
    assert new_fake_journal.games[0].players == ["A", "B", "C", "D", "E"]

def test_gamefix_command_date(fs):
    # pylint: disable=invalid-name, unused-argument
    fake_journal = PickleStore("file")
    date20180409 = dateutil.parser.parse("2018-04-09")

    add_command(("1", "2", "3", "4", "5"), fake_journal, date=date20180409, namespace=None)
    add_command(("11", "22", "33", "44", "5"), fake_journal, date=None, namespace=None)
    gamefix_command(0, fake_journal, ("A", "B", "C", "D", "E"), date=None, namespace=None)
    gamefix_command(1, fake_journal, ("AA", "BB", "CC", "DD", "EE"), date=date20180409,
                    namespace=None)

    new_fake_journal = PickleStore("file")
    new_fake_journal.open()

    assert len(new_fake_journal) == 2
    assert new_fake_journal.games[0].players == ["A", "B", "C", "D", "E"]
    assert new_fake_journal.games[0].date == date20180409
    assert new_fake_journal.games[1].players == ["AA", "BB", "CC", "DD", "EE"]
    assert new_fake_journal.games[1].date == date20180409
