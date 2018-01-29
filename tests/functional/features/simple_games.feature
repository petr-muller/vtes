Feature: Logging simple games

Scenario Outline: Accept games with three to six players
    When I invoke vtes add
    And I specify <count> players
    And I submit the command
    Then command finishes successfuly

    Examples: Vertical
      | count | 3 | 4 | 5 | 6 |

Scenario Outline: Refuse games with not three to six players
    When I invoke vtes add
    And I specify <count> players
    And I submit the command
    Then command finishes unsuccessfuly
    And command emits helpful error message about player count

    Examples: Vertical
      | count | 0 | 1 | 2 | 7 |

Scenario: List logged game
    Given I logged five games
    When I invoke vtes games
    Then command finishes successfuly
    And five games are listed
    And listed games have identifiers

Scenario: Add games with victory points
    When I invoke vtes add
    And I specify players with victory points
    And I submit the command
    Then command finishes successfuly

Scenario Outline: List game with victory points
    Given I logged game with <count> players where <winning> player had all VPs
    When I invoke vtes games
    Then game with <count> players is listed with <winning> player having all VPs and GW

    Examples: Vertical
      | count   | 3 | 5 | 5 | 6 |
      | winning | 2 | 0 | 4 | 3 |
