Feature: Game namespaces

Scenario: Add games with namespace
    When I invoke vtes add
    And I specify players with decks
    And I specify single level namespace
    And I submit the command
    Then command finishes successfully

Scenario: Add games with namespace
    When I invoke vtes add
    And I specify players with decks
    And I specify triple level namespace
    And I submit the command
    Then command finishes successfully
