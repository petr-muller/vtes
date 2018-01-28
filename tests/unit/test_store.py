# I do not have that high criteria for test code
# pylint: disable=missing-docstring

from io import BytesIO
from vtes.store import GameStore, load_store
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
