# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import when, then, scenarios

scenarios('features/decks.feature')

@when('I invoke vtes decks')
def vtes_decks(vtes_command):
    vtes_command.add_arguments(("decks",))

@then('deck statistics are listed')
def listed_deck_rankings(vtes_command):
    output = vtes_command.completed.stdout.split("\n")
    assert output[0].startswith("Deck    Player         GW          VP")
    assert output[1].startswith("------  -------------  ----------  ----------")
    assert output[2].startswith("Deck    Narpas         1/1 (100%)  3/5 (60%)")
    assert output[3].startswith("Deck    sor_garcya     1/1 (100%)  3/5 (60%)")
    assert output[4].startswith("Deck 2  Afri           1/2 (50%)   5/10 (50%)")
