"""Log of a single VtES game"""

import re
import datetime
from typing import Sequence, List
from blessings import Terminal

TERM = Terminal()

def set_colorize(colorize: bool) -> None:
    """Toggle colorizing of __str__ methods of Game"""
    Game.COLORIZE = colorize

PLAYER_PATTERN = r"(?P<name>[^(:]+)(\((?P<deck>.*)\)){0,1}(:(?P<points>\d(\.5){0,1})){0,1}"

class Player:
    """Represents a player result of a game"""
    # pylint: disable=too-few-public-methods
    def __init__(self, name: str, deck: str, points: float) -> None:
        self.name: str = name
        self.deck: str = deck
        self.points: float = points

    def __str__(self) -> str:
        deck = f" ({self.deck})" if self.deck is not None else ""
        points = f" {self.points:g}VP" if self.points else ""
        return self.name + deck + points


def parse_player(raw_player: str) -> Player:
    """Parse a player-in-a-game input

    Example: 'player(deck):3'"""
    match = re.match(PLAYER_PATTERN, raw_player)
    player = match.group("name")
    deck = match.group("deck") or None
    points = int(match.group("points")) if match.group("points") is not None else None

    return Player(player, deck, points)


class Game:
    """Represents a VtES game"""
    # pylint: disable=too-few-public-methods
    COLORIZE = False

    @staticmethod
    def _colorize_player_line(line: str, winner: bool = False, points: float = 0) -> str:
        if winner:
            return TERM.green + line + TERM.normal
        elif points:
            return TERM.bright_red + line + TERM.normal

        return line

    @staticmethod
    def _make_player_line(player: Player, winner: str) -> str:
        player_line = str(player)

        if player.name == winner:
            player_line += " GW"

        if Game.COLORIZE:
            return Game._colorize_player_line(player_line, player.name == winner, player.points)

        return player_line

    @staticmethod
    def from_table(table: Sequence[str], date: datetime.datetime = None) -> 'Game':
        """Parse a table result definition and return a Game instance from it"""
        results: List[Player] = []
        winning_points: float = None
        winner: str = None

        for item in table:
            player = parse_player(item)
            results.append(player)

            points = player.points or 0
            current_winning_points = winning_points or 1

            if points > current_winning_points:
                winning_points = points
                winner = player.name
            elif points == winning_points:
                winning_points = None
                winner = None

        return Game(results, winner, winning_points, date)

    def __init__(self, results: Sequence[Player], winner: str, winning_points: float,
                 date: datetime.datetime) -> None:
        self.winning_points: float = winning_points
        self.winner: str = winner
        self.player_results: Sequence[Player] = results
        self.date: datetime.datetime = date

    @property
    def players(self) -> Sequence[str]:
        """Return a list of player names"""
        return [player.name for player in self.player_results]

    def __str__(self) -> str:
        players = []
        for player in self.player_results:
            players.append(Game._make_player_line(player, self.winner))

        if self.date:
            return "{date}: {results}".format(date=self.date.date().isoformat(),
                                              results=" \u25b6 ".join(players))

        return " \u25b6 ".join(players)
