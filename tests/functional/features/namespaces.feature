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

Scenario: Deck statistics for a given namespace
    Given I logged games with multi level namespace
    And I logged games with different namespaces
    When I invoke vtes decks
    And I specify namespace
    And I submit the command
    Then command finishes successfully
    And deck statistics from games with namespace are listed

Scenario: Stats for a given namespace
    Given I logged games with multi level namespace
    And I logged games with different namespaces
    When I invoke vtes stats
    And I specify namespace
    And I submit the command
    Then command finishes successfully
    And game statistics from games with namespace are listed
