# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name, unused-import

from pytest_bdd import given, when, then, scenarios
from tests.fixtures.commands import vtes_command, five_games

scenarios('features/database.feature')

@when('I invoke vtes add with --journal-db and --journal-file')
def pickle_and_db(tmpdir, vtes_command):
    # pylint: disable=protected-access
    vtes_command._storage = ('--journal-file', tmpdir / 'file', '--journal-db', tmpdir / 'file.db')

@given('I logged five games to database')
@given('I logged some games to database')
def log_some_games(tmpdir, five_games):
    for game in five_games:
        command = vtes_command(tmpdir).with_database().add().with_arguments(game).execute()
        assert command.completed.returncode == 0

@when('I invoke vtes stats with --journal-db')
def vtes_stats(vtes_command):
    vtes_command.with_database().stats()

@when('I invoke vtes add with --journal-db')
def vtes_add_db(vtes_command):
    vtes_command.with_database().add()

@when('I invoke vtes games with --journal-db')
def vtes_games(vtes_command):
    vtes_command.with_database().games()

@when('I invoke vtes decks with --journal-db')
def vtes_decks(vtes_command):
    vtes_command.with_database().decks()

@then('five games are listed')
def five_games_listed(vtes_command):
    output = [line for line in vtes_command.completed.stdout.split("\n") if line]
    assert len(output) == 5

@when('I change game 1 with --journal-db')
def change_game_1(vtes_command):
    vtes_command.with_database().gamefix().with_arguments(("1", "Felipe(dECK):0", "aFRI(Deck):0",
                                                           "XZealot(Deck):3", "Cooper(Deck):1"))
