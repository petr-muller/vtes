# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import then, scenarios

scenarios('features/stats.feature')

@then('stats contain game win ratio for each player')
def game_win_ratios(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    assert output[0].startswith("Player           GW    VP    Games  GW Ratio")
    assert output[2].startswith("Afri              1     6        5  20%")
    assert output[3].startswith("bluedevil         1     4        2  50%")
    assert output[10].startswith("ShaneS_A tier     0     0        2  0%")

@then('stats contain victory point snatch ratio for each player')
def vp_snatch_ratios(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    assert output[0].startswith("Player           GW    VP    Games  GW Ratio    VP Snatch")
    assert output[2].startswith("Afri              1     6        5  20%         25%")
    assert output[3].startswith("bluedevil         1     4        2  50%         40%")
    assert output[6].startswith("XZealot           0     3        3  0%          21%")
    assert output[7].startswith("Cooper            0     2        3  0%          14%")
    assert output[8].startswith("Nebojsa           0     2        2  0%          20%")
    assert output[9].startswith("preston           0     1        1  0%          20%")
    assert output[10].startswith("ShaneS_A tier     0     0        2  0%          0%")
