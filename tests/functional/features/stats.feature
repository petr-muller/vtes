Feature: Game statistics

Scenario: General timeline statistics
    Given I logged some games
    When I invoke vtes stats
    And I submit the command
    Then command finishes successfully
    And player rankings are listed

Scenario: Game Win Ratio
    Given I logged some games
    When I invoke vtes stats
    And I submit the command
    Then command finishes successfully
    And stats contain game win ratio for each player

Scenario: VP Snatch Ratio Given I logged some games
    Given I logged some games
    When I invoke vtes stats
    And I submit the command
    Then command finishes successfully
    And stats contain victory point snatch ratio for each player
