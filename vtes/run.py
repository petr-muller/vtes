"""Entry point for the `vtes` command"""

import pathlib
from argparse import Action, ArgumentParser
import datetime
from typing import Sequence, Union
from tabulate import tabulate
import dateutil.parser

from vtes.game import Game, set_colorize
from vtes.store import PickleStore, DatabaseStore

StorageBackedStore = Union[PickleStore, DatabaseStore]  # pylint: disable=invalid-name

def games_command(journal: StorageBackedStore) -> None:
    """List all games in the store"""
    journal.open()

    set_colorize(True)
    # ugh. automatically compute padding size
    count_size = len(str(len(journal)))
    for index, game in enumerate(journal):
        print(f"{index:{count_size}d}: {game}")


def add_command(players: Sequence[str], journal: StorageBackedStore,
                date: datetime.datetime = None, namespace: str = None) -> None:
    """Create a new Game and add it to the store"""
    try:
        journal.open()
    except FileNotFoundError:
        # No problem, we will create the file when we save
        pass

    game = Game.from_table(players, date=date, namespace=namespace)
    journal.add(game)
    journal.save()


def gamefix_command(game_index: int, players: Sequence[str], journal: StorageBackedStore,
                    date: datetime.datetime = None):
    """Change the properties of an existing game"""
    journal.open()

    if date:
        game = Game.from_table(players, date)
    else:
        game = Game.from_table(players, list(journal)[game_index].date)

    journal.fix(game_index, game)
    journal.save()


def stats_command(journal: StorageBackedStore) -> None:
    """Output various statistics"""
    journal.open()

    rankings = journal.rankings()
    print(tabulate(rankings, headers=('Player', 'GW', 'VP', 'Games', "GW Ratio", "VP Snatch")))
    print("")
    print(f"Overall statistics: {len(journal)} games with {len(rankings)} players")


def decks_command(journal: StorageBackedStore, player: str) -> None:
    """Prints statistics about decks involved in games in store"""
    journal.open()

    deck_rankings = journal.decks(player)
    print(tabulate(deck_rankings, headers=('Deck', 'Player', 'GW', 'VP')))


class ParsePlayerAction(Action):
    """This custom argparse Action parses a list of players"""
    # too-few-public-methods: Action only needs to override __call__
    # pylint: disable=too-few-public-methods
    def __init__(self, *args, **kwargs):
        Action.__init__(self, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if 2 < len(values) < 7:
            setattr(namespace, self.dest, values)
        else:
            raise ValueError("VtES expects three to six players")


def main(): # pragma: no cover
    """Entry point for the `vtes` command"""

    parser = ArgumentParser()

    storage = parser.add_mutually_exclusive_group()
    storage.add_argument("--journal-file", dest="journal", type=PickleStore,
                         default=PickleStore(pathlib.Path.home() / ".vtes-journal"))
    storage.add_argument("--journal-db", dest="journal", type=DatabaseStore)
    subcommands = parser.add_subparsers()

    add = subcommands.add_parser("add")
    add.add_argument("--date", default=None, type=dateutil.parser.parse)
    add.add_argument("--namespace", default=None)
    add.add_argument("players", action=ParsePlayerAction, nargs='*')
    add.set_defaults(func=add_command)

    games = subcommands.add_parser("games")
    games.set_defaults(func=games_command)

    gamefix = subcommands.add_parser("game-fix")
    gamefix.add_argument("game_index", type=int)
    gamefix.add_argument("--date", default=None, type=dateutil.parser.parse)
    gamefix.add_argument("players", action=ParsePlayerAction, nargs='*')
    gamefix.set_defaults(func=gamefix_command)

    decks = subcommands.add_parser("decks")
    decks.add_argument("player", nargs='?', default=None)
    decks.set_defaults(func=decks_command)

    stats = subcommands.add_parser("stats")
    stats.set_defaults(func=stats_command)

    args = parser.parse_args()
    command = args.func
    delattr(args, "func")
    command(**vars(args))

if __name__ == "__main__":
    main() # pragma: no cover
