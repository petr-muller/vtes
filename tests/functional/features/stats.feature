Feature: Game statistics

Scenario: General timeline statistics
    Given I logged some games
    When I invoke vtes stats
    And I submit the command
    Then command finishes successfully
    And player rankings are listed