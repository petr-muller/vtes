# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

import subprocess
import pytest
from pytest_bdd import given, when, then, scenarios

scenarios('features')

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

@when('I invoke vtes add')
def vtes_add(vtes_command):
    vtes_command.add_arguments(('add',))

@when("I specify <count> players")
def x_players(count, vtes_command):
    vtes_command.add_arguments([f"player_{x}" for x in range(int(count))])

@when('I submit the command')
def execute(vtes_command):
    vtes_command.execute()

@then('command finishes successfuly')
def check_command_passed(vtes_command):
    assert vtes_command.completed.returncode == 0

@then('command finishes unsuccessfuly')
def check_command_failed(vtes_command):
    assert vtes_command.completed.returncode != 0

@then('command emits helpful error message about player count')
def check_error_for_player_count(vtes_command):
    assert "three to six players" in vtes_command.completed.stderr

@given('I logged five games')
def log_five_games(tmpdir):
    command = vtes_command(tmpdir)
    command.add_arguments(("add", "one", "two", "three", "four", "five"))
    for _ in range(5):
        command.execute()
        assert command.completed.returncode == 0

@when('I invoke vtes games')
def vtes_games(vtes_command):
    vtes_command.add_arguments(["games"])
    vtes_command.execute()

@then('five games are listed')
def five_games_listed(vtes_command):
    output = [line for line in vtes_command.completed.stdout.split("\n") if line]
    assert len(output) == 5
    for line in output:
        assert line.endswith("one \u25b6 two \u25b6 three \u25b6 four \u25b6 five")
