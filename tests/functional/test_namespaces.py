# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import given, when, scenarios

from tests.fixtures.commands import vtes_command

scenarios('features/namespaces.feature')

@when('I specify single level namespace')
def single_level_namespace(vtes_command):
    vtes_command.with_arguments(("--namespace", "namespace"))

@when('I specify triple level namespace')
def triple_level_namespace(vtes_command):
    vtes_command.with_arguments(("--namespace", "name/spa/ce"))

DECKS_5 = ("Pascek Bruise & Vote", "Synesios Summon History", "Malgorzata", "BH Assamite Rush",
           "Anarchy in the Wild West")
PLAYERS_5 = ("Zerato", "Vladish", "preston", "XZealot", "Afri")

@given('I logged game with namespace')
def log_game_with_namespace(tmpdir):
    arguments = [f"{player}({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("namespace").execute()

@given('I logged game with multi level namespace')
def log_game_with_ml_namespace(tmpdir):
    arguments = [f"{player}({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("name/spa/ce").execute()
