# I do not have that high criteria for test code
# pylint: disable=missing-docstring
import dateutil
from vtes.game import Game, parse_player, set_colorize

def test_parse_player():
    player = parse_player("vtesser")
    assert player.name == "vtesser"
    assert player.points is None
    assert player.deck is None

def test_parse_player_deck():
    player = parse_player("vtesser(!Gangrel Bleed)")
    assert player.name == "vtesser"
    assert player.points is None
    assert player.deck == "!Gangrel Bleed"

def test_parse_player_deck_vp():
    player = parse_player("Afri(Ventrue Lawfirm):3")
    assert player.name == "Afri"
    assert player.points == 3
    assert player.deck == "Ventrue Lawfirm"

def test_parse_player_vp():
    player = parse_player("Afri:4")
    assert player.name == "Afri"
    assert player.points == 4
    assert player.deck is None

def test_game():
    table = ("P1", "P2", "P3", "P4", "P5")
    game = Game.from_table(table)
    assert str(game) == "P1 \u25b6 P2 \u25b6 P3 \u25b6 P4 \u25b6 P5"

def test_game_with_vps():
    table = ("P1:0", "P2:2", "P3:3", "P4", "P5")
    game = Game.from_table(table)

    assert game.players == ["P1", "P2", "P3", "P4", "P5"]
    assert str(game) == "P1 \u25b6 P2 2VP \u25b6 P3 3VP GW \u25b6 P4 \u25b6 P5"
    assert game.winner == "P3"
    assert game.winning_points == 3

def test_game_with_draw():
    table = ("P1:0", "P2:2", "P3:2", "P4:1", "P5")
    game = Game.from_table(table)

    assert game.players == ["P1", "P2", "P3", "P4", "P5"]
    assert str(game) == "P1 \u25b6 P2 2VP \u25b6 P3 2VP \u25b6 P4 1VP \u25b6 P5"
    assert game.winner is None
    assert game.winning_points is None

def test_colorize():
    table = ("P1:0", "P2:2", "P3:3", "P4", "P5")
    game = Game.from_table(table)
    set_colorize(True)
    assert str(game) == "P1 \u25b6 P2 2VP \u25b6 P3 3VP GW \u25b6 P4 \u25b6 P5"
    set_colorize(False)
    assert str(game) == "P1 \u25b6 P2 2VP \u25b6 P3 3VP GW \u25b6 P4 \u25b6 P5"

def test_date():
    table = ("P1:0", "P2:2", "P3:3", "P4", "P5")
    game = Game.from_table(table, date=dateutil.parser.parse("2018-03-20"))
    assert game.date == dateutil.parser.parse("2018-03-20")
    assert str(game) == "2018-03-20: P1 \u25b6 P2 2VP \u25b6 P3 3VP GW \u25b6 P4 \u25b6 P5"

def test_namespace():
    # pylint: disable=line-too-long
    table = ("P1:0", "P2:2", "P3:3", "P4", "P5")
    game = Game.from_table(table, date=dateutil.parser.parse("2018-03-20"), namespace="something")
    assert list(game.namespace) == ["something"]
    assert str(game) == "2018-03-20: P1 \u25b6 P2 2VP \u25b6 P3 3VP GW \u25b6 P4 \u25b6 P5 (something)"

    game = Game.from_table(table, date=dateutil.parser.parse("2018-03-20"), namespace="something/else")
    assert list(game.namespace) == ["something", "else"]
    assert str(game) == "2018-03-20: P1 \u25b6 P2 2VP \u25b6 P3 3VP GW \u25b6 P4 \u25b6 P5 (something/else)"
