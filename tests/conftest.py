# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name, unused-import

from pytest_bdd import given, when, then
from tests.fixtures.commands import vtes_command, five_games

@when('I submit the command')
def execute(vtes_command):
    vtes_command.execute()

@when('I invoke vtes add')
def vtes_add(vtes_command):
    vtes_command.add()

@then('command finishes successfully')
def check_command_passed(vtes_command):
    assert vtes_command.completed.returncode == 0

@then('command finishes unsuccessfully')
def check_command_failed(vtes_command):
    assert vtes_command.completed.returncode != 0

@given('I logged some games')
def log_some_games(tmpdir, five_games):
    for game in five_games:
        command = vtes_command(tmpdir).add().with_arguments(game).execute()
        assert command.completed.returncode == 0

DECKS_5 = ("Pascek Bruise & Vote", "Synesios Summon History", "Malgorzata", "BH Assamite Rush",
           "Anarchy in the Wild West")
PLAYERS_5 = ("Zerato", "Vladish", "preston", "XZealot", "Afri")

@when("I specify players with decks")
def x_players_with_decks(vtes_command):
    arguments = [f"{player}({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    vtes_command.add().with_arguments(arguments)

@then('player rankings are listed')
def listed_player_rankings(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    assert output[0].startswith("Player           GW    VP    Games")
    assert output[1].startswith("-------------  ----  ----  -------")
    assert output[2].startswith("Afri              1     6        5")
    assert output[3].startswith("bluedevil         1     4        2")
    assert output[6].startswith("XZealot           0     3        3")
    assert output[7].startswith("Cooper            0     2        3")
    assert output[8].startswith("Nebojsa           0     2        2")
    assert output[9].startswith("preston           0     1        1")
    assert output[10].startswith("ShaneS_A tier     0     0        2")
    assert output[15] == ""
    assert output[16] == "Overall statistics: 5 games with 13 players"

@then('deck statistics are listed')
def listed_deck_rankings(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    assert output[0].startswith("Deck    Player         GW          VP")
    assert output[1].startswith("------  -------------  ----------  ----------")
    assert output[2].startswith("Deck    Narpas         1/1 (100%)  3/5 (60%)")
    assert output[3].startswith("Deck    sor_garcya     1/1 (100%)  3/5 (60%)")
    assert output[4].startswith("Deck 2  Afri           1/2 (50%)   5/10 (50%)")
