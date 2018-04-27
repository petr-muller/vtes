Feature: Game namespaces

Scenario: Add games with namespace
    When I invoke vtes add
    And I specify players with decks
    And I specify single level namespace
    And I submit the command
    Then command finishes successfully

Scenario: Add games with multilevel namespace
    When I invoke vtes add
    And I specify players with decks
    And I specify triple level namespace
    And I submit the command
    Then command finishes successfully

Scenario: List game with namespace
    Given I logged game with namespace
    When I invoke vtes games
    And I submit the command
    Then game is listed with namespace

Scenario: List game with multi level namespace
    Given I logged game with multi level namespace
    When I invoke vtes games
    And I submit the command
    Then game is listed with multi level namespace
