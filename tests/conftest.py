# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import given, when, then
from tests.fixtures.commands import vtes_command

@when('I submit the command')
def execute(vtes_command):
    vtes_command.execute()

@then('command finishes successfully')
def check_command_passed(vtes_command):
    assert vtes_command.completed.returncode == 0

@given('I logged some games')
def log_some_games(tmpdir):
    games = (("Zerato(Deck):0", "preston(Deck):1", "Afri(Deck):0", "XZealot(Deck):0",
              "bluedevil(Deck):4"),
             ("Felipe(Deck):0", "Afri(Deck):0", "XZealot(Deck):2", "Cooper(Deck):2"),
             ("bluedevil(Deck):0", "XZealot(Deck):1", "Narpas(Deck):3", "gNat(Deck):0",
              "Afri(Deck):1"),
             ("Afri(Deck 2):3", "Nebojsa(Deck):2", "ShaneS_A tier(Deck):0", "Blooded(Deck):0",
              "Cooper(Deck):0"),
             ("Afri(Deck 2):2", "sor_garcya(Deck):3", "Cooper(Deck)", "ShaneS_A tier(Deck):0",
              "Nebojsa(Deck):0"))
    for game in games:
        command = vtes_command(tmpdir)
        command.add_arguments(("add",) + game)
        command.execute()
        assert command.completed.returncode == 0
