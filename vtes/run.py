"""Entry point for the `vtes` command"""

import pathlib
from argparse import Action, ArgumentParser
import datetime
from typing import Sequence, Union, Optional
from tabulate import tabulate
import dateutil.parser

from vtes.game import Game, set_colorize, parse_namespace, GameNamespace
from vtes.store import PickleStore, DatabaseStore, DeckRanking, Ranking

StorageBackedStore = Union[PickleStore, DatabaseStore]  # pylint: disable=invalid-name

def games_command(journal: StorageBackedStore, namespace: Optional[GameNamespace]) -> None:
    """List all games in the store"""
    journal.open()

    set_colorize(True)
    # ugh. automatically compute padding size
    games = list(journal.filter(namespace=namespace))
    count_size = len(str(len(games)))
    for index, game in enumerate(games):
        print(f"{index:{count_size}d}: {game}")


def add_command(players: Sequence[str], journal: StorageBackedStore,
                date: datetime.datetime, namespace: Optional[GameNamespace]) -> None:
    """Create a new Game and add it to the store"""
    try:
        journal.open()
    except FileNotFoundError:
        # No problem, we will create the file when we save
        pass

    game = Game.from_table(players, date=date, namespace=namespace)
    journal.add(game)
    journal.save()


def gamefix_command(game_index: int, journal: StorageBackedStore, players: Sequence[str],
                    date: datetime.datetime, namespace: Optional[GameNamespace]) -> None:
    """Change the properties of an existing game"""
    journal.open()

    old = list(journal)[game_index]

    game = Game.from_table(players) if players else old
    game.date = date or old.date
    game.namespace = namespace or old.namespace

    journal.fix(game_index, game)
    journal.save()


def stats_command(journal: StorageBackedStore, namespace: Optional[GameNamespace]) -> None:
    """Output various statistics"""
    journal.open()
    rankings = journal.rankings(namespace=namespace)

    print(tabulate(rankings, headers=Ranking.HEADERS))
    print("")
    print(f"Overall statistics: {len(journal)} games with {len(rankings)} players")


def decks_command(journal: StorageBackedStore, player: str,
                  namespace: Optional[GameNamespace]) -> None:
    """Prints statistics about decks involved in games in store"""
    journal.open()
    deck_rankings = journal.decks(player=player, namespace=namespace)
    print(tabulate(deck_rankings, headers=DeckRanking.HEADERS))


class ParsePlayerAction(Action):
    """This custom argparse Action parses a list of players"""
    # too-few-public-methods: Action only needs to override __call__
    # pylint: disable=too-few-public-methods
    def __init__(self, *args, **kwargs):
        Action.__init__(self, *args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        if 2 < len(values) < 7 or namespace.func is gamefix_command:
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
    add.add_argument("--namespace", default=None, type=parse_namespace)
    add.add_argument("players", action=ParsePlayerAction, nargs='*')
    add.set_defaults(func=add_command)

    games = subcommands.add_parser("games")
    games.add_argument("--namespace", default=None, type=parse_namespace)
    games.set_defaults(func=games_command)

    gamefix = subcommands.add_parser("game-fix")
    gamefix.add_argument("game_index", type=int)
    gamefix.add_argument("--date", default=None, type=dateutil.parser.parse)
    gamefix.add_argument("--namespace", default=None, type=parse_namespace)
    gamefix.add_argument("players", action=ParsePlayerAction, nargs='*')
    gamefix.set_defaults(func=gamefix_command)

    decks = subcommands.add_parser("decks")
    decks.add_argument("player", nargs='?', default=None)
    decks.add_argument("--namespace", default=None, type=parse_namespace)
    decks.set_defaults(func=decks_command)

    stats = subcommands.add_parser("stats")
    stats.add_argument("--namespace", default=None, type=parse_namespace)
    stats.set_defaults(func=stats_command)

    args = parser.parse_args()

    command = args.func
    delattr(args, "func")
    command(**vars(args))

if __name__ == "__main__":
    main() # pragma: no cover
