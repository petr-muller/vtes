Feature: Logging simple games

Scenario Outline: Log a single game
    When I invoke vtes add
    And I specify first player <p1> playing <deck_1> with <VP1> victory points
    And I specify second player <p2> playing <deck_2> with <VP2> victory points
    And I specify third player <p3> playing <deck_3> with <VP3> victory points
    And I specify fourth player <p4> playing <deck_4> with <VP4> victory points
    And I specify fifth player <p5> playing <deck_5> with <VP5> victory points
    And I submit the command
    Then command finishes successfuly

    Examples: Vertical
      | p1     | Troile  |
      | p2     | Mithras |
      | p3     | Anatole |
      | p4     | Xaviar  |
      | p5     | Villon  |
      | deck_1 | Eurobrujah |
      | deck_2 | Ventrue Lawfirm |
      | deck_3 | DEM SB |
      | deck_4 | PRO Wall |
      | deck_5 | Aching Beauty |
      | VP1    | 1 |
      | VP2    | 0 |
      | VP3    | 1 |
      | VP4    | 1.5 |
      | VP5    | 1.5 |
