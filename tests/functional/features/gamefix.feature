Feature: Game Fix

Scenario: Fix existing game
    Given I logged some games
    When I change game 1
    And I submit the command
    Then command finishes successfully
    And game is changed

Scenario: Change game date
    Given I logged some games
    When I change date of game 1
    And I submit the command
    Then command finishes successfully
    And game date is changed

Scenario: Change game namespace
    Given I logged some games
    When I change namespace of game 1
    And I submit the command
    Then command finishes successfully
    And game namespace is changed
