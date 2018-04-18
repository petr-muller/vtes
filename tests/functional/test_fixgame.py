# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import when, then, scenarios

from tests.fixtures.commands import vtes_command

scenarios('features/gamefix.feature')

@when('I change game 1')
def change_game_1(vtes_command):
    vtes_command.gamefix().with_arguments(("1", "Felipe(dECK):0", "aFRI(Deck):0", "XZealot(Deck):3",
                                           "Cooper(Deck):1"))

@then('game is changed')
def game_is_changed(tmpdir):
    command = vtes_command(tmpdir).games().execute()

    output = [line for line in command.completed.stdout.split("\n") if line]
    assert output[1] == "1: Felipe (dECK) \u25b6 aFRI (Deck) \u25b6 XZealot (Deck) 3VP GW \u25b6 Cooper (Deck) 1VP" # pylint: disable=line-too-long
