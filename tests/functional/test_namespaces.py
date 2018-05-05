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
POINTS_5 = (0, 1, 1, 0, 3)

@given('I logged game with namespace')
def log_game_with_namespace(tmpdir):
    arguments = [f"{player}({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("namespace").execute()

@given('I logged game with multi level namespace')
def log_game_with_ml_namespace(tmpdir):
    arguments = [f"{player}({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("name/spa/ce").execute()

@given('I logged games with multi level namespace')
def log_games_with_ml_namespace(tmpdir):
    arguments = [f"{player}({deck}):{points}" for player, deck, points in zip(PLAYERS_5,
                                                                              DECKS_5,
                                                                              POINTS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("name/spa/ce").execute()
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("name/spa/de").execute()
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("name").execute()

@given('I logged games with different namespaces')
def log_games_with_diff_namespaces(tmpdir):
    arguments = [f"{player}({deck}):{points}" for player, deck, points in zip(PLAYERS_5,
                                                                              DECKS_5,
                                                                              POINTS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).namespace("different/spa/ce").execute()
    vtes_command(tmpdir).add().with_arguments(arguments).execute()
