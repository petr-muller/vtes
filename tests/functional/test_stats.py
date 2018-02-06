# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import given, when, then, scenarios
from tests.fixtures.commands import vtes_command

scenarios('features/stats.feature')

@given('I logged some games')
def log_some_games(tmpdir):
    games = (("Zerato:0", "preston:1", "Afri:0", "XZealot:0", "bluedevil:4"),
             ("Felipe:0", "Afri:0", "XZealot:2", "Cooper:2"),
             ("bluedevil:0", "XZealot:1", "Narpas:3", "gNat:0", "Afri:1"),
             ("Afri:3", "Nebojsa:2", "ShaneS_A tier:0", "Blooded:0", "Cooper:0"),
             ("Afri:2", "sor_garcya:3", "Cooper", "ShaneS_A tier:0", "Nebojsa:0"))
    for game in games:
        command = vtes_command(tmpdir)
        command.add_arguments(("add",) + game)
        command.execute()
        assert command.completed.returncode == 0

@when('I invoke vtes stats')
def vtes_stats(vtes_command):
    vtes_command.add_arguments(("stats",))

@then('player rankings are listed')
def listed_player_rankings(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    print(output)
    assert output[0] == "Player           GW    VP    Games"
    assert output[1] == "-------------  ----  ----  -------"
    assert output[2] == "Afri              1     6        5"
    assert output[3] == "bluedevil         1     4        2"
    assert "Narpas            1     3        1" in output[4:6]
    assert "sor_garcya        1     3        1" in output[4:6]
    assert output[6] == "XZealot           0     3        3"
    assert output[7] == "Cooper            0     2        3"
    assert output[8] == "Nebojsa           0     2        2"
    assert output[9] == "preston           0     1        1"
    assert output[10] == "ShaneS_A tier     0     0        2"
    assert "Zerato            0     0        1" in output[11:]
    assert "Felipe            0     0        1" in output[11:]
    assert "gNat              0     0        1" in output[11:]
    assert "Blooded           0     0        1" in output[11:]
