# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from random import randrange

from pytest_bdd import given, when, then, scenarios

from tests.fixtures.commands import vtes_command

scenarios('features/simple_games.feature')

@when("I specify <count> players")
def x_players(count, vtes_command):
    vtes_command.with_arguments([f"player_{x}" for x in range(int(count))])

@when("I specify players with victory points")
def x_players_with_vps(vtes_command):
    count = 5
    points = [0] * count
    points[randrange(count)] = count
    vtes_command.with_arguments([f"player_{x}:{points[x]}" for x in range(int(count))])

DECKS_5 = ("Pascek Bruise & Vote", "Synesios Summon History", "Malgorzata", "BH Assamite Rush",
           "Anarchy in the Wild West")
PLAYERS_5 = ("Zerato", "Vladish", "preston", "XZealot", "Afri")

@when("I specify players with decks and victory points")
def x_players_with_decks_and_vps(vtes_command):
    points = (2, 0, 0, 1, 2)
    arguments = [f"{player}({deck}):{vp}" for player, deck, vp in zip(PLAYERS_5, DECKS_5, points)]
    vtes_command.add().with_arguments(arguments)

@then('command emits helpful error message about player count')
def check_error_for_player_count(vtes_command):
    assert "three to six players" in vtes_command.completed.stderr

@given('I logged five games')
def log_five_games(tmpdir):
    command = vtes_command(tmpdir).add().with_arguments(("one", "two", "three", "four", "five"))
    for _ in range(5):
        command.execute()
        assert command.completed.returncode == 0

@given('I logged game with <count> players where <winning> player had all VPs')
def log_game_with_vp(tmpdir, count, winning):
    count = int(count)
    winning = int(winning)

    points = [0] * count
    points[winning] = count
    players = [f"player_{x}:{points[x]}" for x in range(count)]
    vtes_command(tmpdir).add().with_arguments(players).execute()

@given('I logged game with decks and victory points')
def log_game_with_decks_and_vp(tmpdir):
    points = (2, 0, 0, 1, 2)
    arguments = [f"{player}({deck}):{vp}" for player, deck, vp in zip(PLAYERS_5, DECKS_5, points)]
    vtes_command(tmpdir).add().with_arguments(arguments).execute()

@given('I logged game with decks')
def log_game_with_decks(tmpdir):
    arguments = [f"{player}({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    vtes_command(tmpdir).add().with_arguments(arguments).execute()

@then('five games are listed')
def five_games_listed(vtes_command):
    output = [line for line in vtes_command.completed.stdout.split("\n") if line]
    assert len(output) == 5
    for line in output:
        assert line.endswith("one \u25b6 two \u25b6 three \u25b6 four \u25b6 five")

@then('listed games have identifiers')
def identifiers(vtes_command):
    output = [line for line in vtes_command.completed.stdout.split("\n") if line]
    assert len(output) == 5
    for item, line in enumerate(output):
        assert line.startswith(f"{item}: ")

@then('game with <count> players is listed with <winning> player having all VPs and GW')
def list_game_with_vp(vtes_command, count, winning):
    count = int(count)
    winning = int(winning)

    players = [f"player_{x}" for x in range(count)]
    players[winning] = f"{players[winning]} {count}VP GW"
    players = " \u25b6 ".join(players)

    output = vtes_command.completed.stdout
    assert output.startswith(f"0: {players}")

@then('game is listed with decks and victory points')
def decks_and_victory_points(vtes_command):
    points = [f" {vp}VP" if vp else "" for vp in (2, 0, 0, 1, 2)]
    players = [f"{player} ({deck}){vp}" for player, deck, vp in zip(PLAYERS_5, DECKS_5, points)]
    players = " \u25b6 ".join(players)
    output = vtes_command.completed.stdout
    assert output.startswith(f"0: {players}")

@then('game is listed with decks')
def decks(vtes_command):
    players = [f"{player} ({deck})" for player, deck in zip(PLAYERS_5, DECKS_5)]
    players = " \u25b6 ".join(players)
    output = vtes_command.completed.stdout
    assert output.startswith(f"0: {players}")

@when('I specify game date')
def game_dates(vtes_command):
    vtes_command.with_arguments(("--date", "2018-03-22"))
