# missing-docstring, because we do not need docstring for each test method
# redefined-outer-name: fixtures unfortunately trigger this
# pylint: disable=missing-docstring, redefined-outer-name

from pytest_bdd import when, scenarios

scenarios('features/namespaces.feature')

@when('I specify single level namespace')
def single_level_namespace(vtes_command):
    vtes_command.with_arguments(("--namespace", "namespace"))

@when('I specify triple level namespace')
def triple_level_namespace(vtes_command):
    vtes_command.with_arguments(("--namespace", "name/spa/ce"))
