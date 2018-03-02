# I do not have that high criteria for test code
# pylint: disable=missing-docstring

from io import BytesIO
from vtes.store import GameStore, load_store, Ranking
from vtes.game import Game

def test_store():
    store = GameStore()
    assert len(store) == 0  # pylint: disable=len-as-condition
    store.add(Game(("1", "2", "3", "4", "5")))
    assert len(store) == 1
    store.add(Game(("A", "B", "C", "D", "E")))
    assert len(store) == 2

    games = list(store)
    assert str(games[0]) == "1 \u25b6 2 \u25b6 3 \u25b6 4 \u25b6 5"
    assert str(games[1]) == "A \u25b6 B \u25b6 C \u25b6 D \u25b6 E"

def test_store_save_load():
    store = GameStore()
    store.add(Game(("1", "2", "3", "4", "5")))
    store.add(Game(("A", "B", "C", "D", "E")))

    with BytesIO() as fakefile:
        store.save(fakefile)
        fakefile.seek(0, 0)
        new_store = load_store(fakefile)

    assert len(new_store) == 2
    games = list(new_store)
    assert str(games[0]) == "1 \u25b6 2 \u25b6 3 \u25b6 4 \u25b6 5"
    assert str(games[1]) == "A \u25b6 B \u25b6 C \u25b6 D \u25b6 E"

def test_rankings():
    ranking = Ranking("player", 0, 0, 0)
    ranking_same = Ranking("player", 0, 0, 0)
    assert ranking.player == "player"
    assert ranking.wins == 0
    assert ranking.points == 0
    assert ranking.games == 0
    assert ranking.gw_ratio is None
    assert str(ranking) == "player GW=0 VP=0 games=0"
    assert repr(ranking) == "player GW=0 VP=0 games=0"

    assert ranking == ranking
    assert ranking == ranking_same

    ranking = Ranking("player1", 1, 2.5, 3)
    assert ranking.player == "player1"
    assert ranking.wins == 1
    assert ranking.points == 2.5
    assert ranking.games == 3
    assert ranking.gw_ratio == 33
    assert ranking != ranking_same
    assert ranking == ranking

def test_rankings_comparison():
    assert Ranking("one", 1, 3, 3) > Ranking("two", 0, 4, 4)
    assert Ranking("one", 1, 5, 3) > Ranking("two", 1, 4, 4)
    assert Ranking("one", 1, 4, 5) > Ranking("two", 1, 4, 4)

def test_store_rankings():
    store = GameStore()
    store.add(Game(("1:3", "2:1", "3:1", "4", "5")))
    store.add(Game(("A:4", "2:1", "C", "D", "E")))
    rankings = store.rankings()
    assert len(rankings) == 9
    assert rankings[0] == Ranking("A", 1, 4, 1)
    assert rankings[1] == Ranking("1", 1, 3, 1)
    assert rankings[2] == Ranking("2", 0, 2, 2)
    assert rankings[3] == Ranking("3", 0, 1, 1)
    for loser in ("4", "5", "C", "D", "E"):
        assert Ranking(loser, 0, 0, 1) in rankings

def test_gw_ratio():
    assert Ranking("aaa", 0, 0, 0).gw_ratio is None
    assert Ranking("aaa", 1, 4, 1).gw_ratio == 100
    assert Ranking("aaa", 1, 4, 2).gw_ratio == 50
    assert Ranking("aaa", 1, 4, 3).gw_ratio == 33
    assert Ranking("aaa", 2, 4, 3).gw_ratio == 67

    ranking = Ranking("aaa", 0, 0, 0)
    ranking.games = 3
    ranking.wins = 2
    assert ranking.gw_ratio == 67
