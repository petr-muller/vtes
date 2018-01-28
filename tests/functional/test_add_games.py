# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

import subprocess
import pytest
from pytest_bdd import when, then, scenarios

scenarios('features')

class Executable:
    def __init__(self, command=()):
        self.command = list(command)
        self.completed = None

    def add_arguments(self, arguments):
        self.command.extend(arguments)

    def execute(self):
        self.completed = subprocess.run(self.command, stderr=subprocess.PIPE, encoding='utf-8')

@pytest.fixture
def vtes_command():
    return Executable(("python", "-m", "vtes.run"))

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
