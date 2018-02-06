# missing-docstring, because we do not need docstring for each test method
# pylint: disable=missing-docstring, redefined-outer-name

import subprocess
import pytest

class Executable:
    def __init__(self, command=()):
        self.command = list(command)
        self.completed = None

    def add_arguments(self, arguments):
        self.command.extend(arguments)

    def execute(self):
        self.completed = subprocess.run(self.command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, encoding='utf-8')

@pytest.fixture
def vtes_command(tmpdir):
    journal = tmpdir.join('vtes-journal')
    return Executable(("python", "-m", "vtes.run", "--journal-file", str(journal)))
