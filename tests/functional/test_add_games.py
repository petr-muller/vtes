import subprocess
import pytest
from pytest_bdd import given, when, then, scenarios, parsers

scenarios('features')

class Executable:
    def __init__(self, command=()):
        self.command = list(command)
        self.completed = None
    
    def add_arguments(self, arguments):
        self.command.extend(arguments)

    def execute(self):
        self.completed = subprocess.run(self.command)

@pytest.fixture
def vtes_command():
    return Executable(("python", "-m", "vtes.run"))

@when('I invoke vtes add')
def vtes_add(vtes_command):
    return vtes_command.add_arguments(('add',))

@when('I specify first player <p1> playing <deck_1> with <VP1> victory points')
def player_1(p1, deck_1, VP1, vtes_command):
    return vtes_command.add_arguments((p1, deck_1, VP1))

@when('I specify second player <p2> playing <deck_2> with <VP2> victory points')
def player_2(p2, deck_2, VP2, vtes_command):
    return vtes_command.add_arguments((p2, deck_2, VP2))

@when('I specify third player <p3> playing <deck_3> with <VP3> victory points')
def player_3(p3, deck_3, VP3, vtes_command):
    return vtes_command.add_arguments((p3, deck_3, VP3))

@when('I specify fourth player <p4> playing <deck_4> with <VP4> victory points')
def player_4(p4, deck_4, VP4, vtes_command):
    return vtes_command.add_arguments((p4, deck_4, VP4))

@when('I specify fifth player <p5> playing <deck_5> with <VP5> victory points')
def player_5(p5, deck_5, VP5, vtes_command):
    return vtes_command.add_arguments((p5, deck_5, VP5))

@when('I submit the command')
def execute(vtes_command):
    print(vtes_command.command)
    vtes_command.execute()

@then('command finishes successfuly')
def check_command(vtes_command):
    assert vtes_command.completed.returncode == 0
