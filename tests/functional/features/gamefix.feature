Feature: Game Fix

Scenario: Fix existing game
    Given I logged some games
    When I invoke vtes game-fix
    And I change game 1
    And I submit the command
    Then command finishes successfully
    Then game is changed
