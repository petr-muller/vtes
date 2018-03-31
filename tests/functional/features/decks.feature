Feature: Decks statistics

Scenario: General deck statistics
    Given I logged some games
    When I invoke vtes decks
    And I submit the command
    Then command finishes successfully
    And deck statistics are listed

Scenario: Deck statistics for a single player
    Given I logged some games
    When I invoke vtes decks
    And I specify a single player
    And I submit the command
    Then command finishes successfully
    And deck statistics are listed for a single player
