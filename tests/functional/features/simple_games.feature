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
