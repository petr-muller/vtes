Feature: Store VtES journal in a database

Scenario: Add game to a database
    When I invoke vtes add with --journal-db
    And I specify players with decks
    And I submit the command
    Then command finishes successfully

Scenario: List games from a database
    Given I logged five games to database
    When I invoke vtes games with --journal-db
    And I submit the command
    Then command finishes successfully
    And five games are listed

Scenario: Deck statistics from a database
    Given I logged some games to database
    When I invoke vtes decks with --journal-db
    And I submit the command
    Then command finishes successfully
    And deck statistics are listed

Scenario: General timeline statistics from a database
    Given I logged some games to database
    When I invoke vtes stats with --journal-db
    And I submit the command
    Then command finishes successfully
    And player rankings are listed

Scenario: Database and pickle are mutually exclusive
    When I invoke vtes add with --journal-db and --journal-file
    And I specify players with decks
    And I submit the command
    Then command finishes unsuccessfully

Scenario: List game with namespace from a database
    Given I logged game with namespace to database
    When I invoke vtes games with --journal-db
    And I submit the command
    Then game is listed with namespace

Scenario: List game with multi level namespace from a database
    Given I logged game with multi level namespace to database
    When I invoke vtes games with --journal-db
    And I submit the command
    Then game is listed with multi level namespace

Scenario: List game with multi level namespace from a database
    Given I logged game with multi level namespace to database
    And I logged five games to database
    When I invoke vtes games with --journal-db
    And I specify namespace
    And I submit the command
    Then command finishes successfully
    And only games with namespace are listed

    # This will need Games to have IDs
    # Scenario: Fix existing game in a database
    # Given I logged some games to database
    # When I change game 1 with --journal-db
    # And I submit the command
    # Then command finishes successfully
    # Then game is changed
