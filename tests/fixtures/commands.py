# missing-docstring, because we do not need docstring for each test method
# pylint: disable=missing-docstring, redefined-outer-name

import subprocess
import pytest

class VTESRunnerProxy():
    def __init__(self, tmpdir):
        self.base = ("python", "-m", "vtes.run")
        self.tmpdir = tmpdir
        self._storage = ("--journal-file", str(self.tmpdir / "journal"))
        self._vtes_command = []
        self.completed = None

    def with_pickle_file(self):
        self._storage = ("--journal-file", str(self.tmpdir / "journal"))
        return self

    def with_database(self):
        self._storage = ("--journal-db", str(self.tmpdir / "journal"))
        return self

    def add(self):
        self._vtes_command = ["add"]
        return self

    def stats(self):
        self._vtes_command = ["stats"]
        return self

    def gamefix(self):
        self._vtes_command = ["game-fix"]
        return self

    def games(self):
        self._vtes_command = ["games"]
        return self

    def decks(self):
        self._vtes_command = ["decks"]
        return self

    def with_arguments(self, arguments):
        self._vtes_command.extend(arguments)
        return self

    def execute(self):
        print(self.base + self._storage + tuple(self._vtes_command))
        self.completed = subprocess.run(self.base + self._storage + tuple(self._vtes_command),
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        encoding='utf-8')
        return self

@pytest.fixture
def vtes_command(tmpdir):
    return VTESRunnerProxy(tmpdir)

@pytest.fixture
def five_games():
    return (("Zerato(Deck):0", "preston(Deck):1", "Afri(Deck):0", "XZealot(Deck):0",
             "bluedevil(Deck):4"),
            ("Felipe(Deck):0", "Afri(Deck):0", "XZealot(Deck):2", "Cooper(Deck):2"),
            ("bluedevil(Deck):0", "XZealot(Deck):1", "Narpas(Deck):3", "gNat(Deck):0",
             "Afri(Deck):1"),
            ("Afri(Deck 2):3", "Nebojsa(Deck):2", "ShaneS_A tier(Deck):0", "Blooded(Deck):0",
             "Cooper(Deck):0"),
            ("Afri(Deck 2):2", "sor_garcya(Deck):3", "Cooper(Deck)", "ShaneS_A tier(Deck):0",
             "Nebojsa(Deck):0"))
