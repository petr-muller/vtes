# I do not have that high criteria for test code
# pylint: disable=missing-docstring

from vtes.store import GameStore, Ranking, DeckRanking, PickleStore
from vtes.game import Game

def test_store():
    store = GameStore()
    assert len(store) == 0  # pylint: disable=len-as-condition
    store.add(Game.from_table(("1", "2", "3", "4", "5")))
    assert len(store) == 1
    store.add(Game.from_table(("A", "B", "C", "D", "E")))
    assert len(store) == 2

    games = list(store)
    assert str(games[0]) == "1 \u25b6 2 \u25b6 3 \u25b6 4 \u25b6 5"
    assert str(games[1]) == "A \u25b6 B \u25b6 C \u25b6 D \u25b6 E"

def test_fix():
    store = GameStore()
    store.add(Game.from_table(("1", "2", "3", "4", "5")))
    store.fix(0, Game.from_table(("A", "B", "C", "D", "E")))

    assert len(store) == 1
    games = list(store)
    assert str(games[0]) == "A \u25b6 B \u25b6 C \u25b6 D \u25b6 E"

def test_deck_rankings():
    deck_ranking = DeckRanking("Valkyries", "Afri", 2, 3, 6, 15)
    assert deck_ranking.player == "Afri"
    assert deck_ranking.deck == "Valkyries"
    assert deck_ranking.games == 3
    assert deck_ranking.gw == 2
    assert deck_ranking.gw_ratio == 67
    assert deck_ranking.vp == 6
    assert deck_ranking.vp_total == 15
    assert deck_ranking.vp_ratio == 40

    assert deck_ranking == DeckRanking("Valkyries", "Afri", 2, 3, 6, 15)
    assert str(deck_ranking) == "Valkyries(Afri) 2/3 GW 6/15 VP"
    assert str(deck_ranking) == repr(deck_ranking)

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
    store.add(Game.from_table(("1:3", "2:1", "3:1", "4", "5")))
    store.add(Game.from_table(("A:4", "2:1", "C", "D", "E")))
    rankings = store.rankings()
    assert len(rankings) == 9
    assert rankings[0] == Ranking("A", 1, 4, 1)
    assert rankings[1] == Ranking("1", 1, 3, 1)
    assert rankings[2] == Ranking("2", 0, 2, 2)
    assert rankings[3] == Ranking("3", 0, 1, 1)
    for loser in ("4", "5", "C", "D", "E"):
        assert Ranking(loser, 0, 0, 1) in rankings

def test_store_deck_rankings():
    store = GameStore()
    store.add(Game.from_table(("1(A):3", "2(B):1", "3(C):1", "4(D)", "5"), namespace="na/me/space"))
    store.add(Game.from_table(("A(A):4", "2(B):1", "C(C)", "D", "E"), namespace="na/me/spade"))
    rankings = store.decks(player=None)
    assert len(rankings) == 6
    assert rankings[0] == DeckRanking("A", "A", 1, 1, 4, 5)
    assert rankings[1] == DeckRanking("A", "1", 1, 1, 3, 5)
    assert rankings[2] == DeckRanking("B", "2", 0, 2, 2, 10)
    assert rankings[3] == DeckRanking("C", "3", 0, 1, 1, 5)

    player_rankings = store.decks(player="2")
    assert len(player_rankings) == 1
    assert player_rankings[0] == DeckRanking("B", "2", 0, 2, 2, 10)

    store.add(Game.from_table(("A(AA):3", "2(BB):1", "C(CC):1", "D", "E"), namespace="diff/er/ent"))
    deck_rankings = store.decks(namespace="na/me/space")
    assert len(deck_rankings) == 4
    assert deck_rankings[0] == DeckRanking("A", "1", 1, 1, 3, 5)

    deck_rankings = store.decks(namespace="na")
    assert len(deck_rankings) == 6
    assert deck_rankings[0] == DeckRanking("A", "A", 1, 1, 4, 5)

    deck_rankings = store.decks(player="2", namespace="na/me/spade")
    assert len(deck_rankings) == 1
    assert deck_rankings[0] == DeckRanking("B", "2", 0, 1, 1, 5)


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

def test_vp_snatch():
    ranking = Ranking("aaa", 2, 4, 3)
    assert ranking.vp_ratio is None
    ranking.vp_total = 10
    assert ranking.vp_ratio == 40

def test_picklestore_save_load(fs): # pylint: disable=unused-argument, invalid-name
    store = PickleStore("file")
    store.add(Game.from_table(("1", "2", "3", "4", "5")))
    store.add(Game.from_table(("A", "B", "C", "D", "E")))
    store.save()

    new_store = PickleStore("file")
    new_store.open()

    assert len(new_store) == 2
    games = list(new_store)
    assert str(games[0]) == "1 \u25b6 2 \u25b6 3 \u25b6 4 \u25b6 5"
    assert str(games[1]) == "A \u25b6 B \u25b6 C \u25b6 D \u25b6 E"
