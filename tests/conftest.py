# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import when, then

@when('I submit the command')
def execute(vtes_command):
    vtes_command.execute()

@then('command finishes successfully')
def check_command_passed(vtes_command):
    assert vtes_command.completed.returncode == 0
