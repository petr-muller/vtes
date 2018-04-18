# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import when, then, scenarios

scenarios('features/decks.feature')

@when('I invoke vtes decks')
def vtes_decks(vtes_command):
    vtes_command.decks()

@when("I specify a single player")
def single_player_decks(vtes_command):
    vtes_command.with_arguments(("Afri",))

@then('deck statistics are listed for a single player')
def single_player_deck_rankings(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    assert output[0].startswith("Deck    Player    GW         VP")
    assert output[1].startswith("------  --------  ---------  ----------")
    assert output[2].startswith("Deck 2  Afri      1/2 (50%)  5/10 (50%)")
    assert output[3].startswith("Deck    Afri      0/3 (0%)   1/14 (7%)")
