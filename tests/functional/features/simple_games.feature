Feature: Logging simple games

Scenario Outline: Accept games with three to six players
    When I invoke vtes add
    And I specify <count> players
    And I submit the command
    Then command finishes successfully

    Examples: Vertical
      | count | 3 | 4 | 5 | 6 |

Scenario Outline: Refuse games with not three to six players
    When I invoke vtes add
    And I specify <count> players
    And I submit the command
    Then command finishes unsuccessfully
    And command emits helpful error message about player count

    Examples: Vertical
      | count | 0 | 1 | 2 | 7 |

Scenario: List logged game
    Given I logged five games
    When I invoke vtes games
    And I submit the command
    Then command finishes successfully
    And five games are listed
    And listed games have identifiers

Scenario: Add games with victory points
    When I invoke vtes add
    And I specify players with victory points
    And I submit the command
    Then command finishes successfully

Scenario: Add games with decks
    When I invoke vtes add
    And I specify players with decks
    And I submit the command
    Then command finishes successfully

Scenario: Add games with decks and victory points
    When I invoke vtes add
    And I specify players with decks and victory points
    And I submit the command
    Then command finishes successfully

Scenario Outline: List game with victory points
    Given I logged game with <count> players where <winning> player had all VPs
    When I invoke vtes games
    And I submit the command
    Then game with <count> players is listed with <winning> player having all VPs and GW

    Examples: Vertical
      | count   | 3 | 5 | 5 | 6 |
      | winning | 2 | 0 | 4 | 3 |

Scenario: List game with decks
    Given I logged game with decks
    When I invoke vtes games
    And I submit the command
    Then game is listed with decks

Scenario: List game with decks and victory points
    Given I logged game with decks and victory points
    When I invoke vtes games
    And I submit the command
    Then game is listed with decks and victory points

Scenario: Add games with date
    When I invoke vtes add
    And I specify players with decks
    And I specify game date
    And I submit the command
    Then command finishes successfully
