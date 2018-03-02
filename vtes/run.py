"""Entry point for the `vtes` command"""

import pathlib
from argparse import Action, ArgumentParser
from typing import Sequence
from tabulate import tabulate
from vtes.game import Game, set_colorize
from vtes.store import load_store, GameStore

def games_command(journal_path: pathlib.Path) -> None:
    """List all games in the store"""
    with journal_path.open('rb') as journal_file:
        store = load_store(journal_file)

    set_colorize(True)
    # ugh. automatically compute padding size
    count_size = len(str(len(store)))
    for index, game in enumerate(store):
        print(f"{index:{count_size}d}: {game}")


def add_command(players: Sequence[str], journal_path: pathlib.Path) -> None:
    """Create a new Game and add it to the store"""
    if journal_path.exists():
        with journal_path.open('rb') as journal_file:
            store = load_store(journal_file)
    else:
        store = GameStore()

    game = Game(players)
    store.add(game)

    with journal_path.open('wb') as journal_file:
        store.save(journal_file)


def stats_command(journal_path: pathlib.Path) -> None:
    """Output various statistics"""
    with journal_path.open('rb') as journal_file:
        store = load_store(journal_file)

    rankings = store.rankings()
    print(tabulate(rankings, headers=('Player', 'GW', 'VP', 'Games', "GW Ratio", "VP Snatch")))
    print("")
    print(f"Overall statistics: {len(store)} games with {len(rankings)} players")


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
    parser.add_argument("--journal-file", dest="journal_path",
                        default=pathlib.Path.home() / ".vtes-journal", type=pathlib.Path)
    subcommands = parser.add_subparsers()

    add = subcommands.add_parser("add")
    add.add_argument("players", action=ParsePlayerAction, nargs='*')
    add.set_defaults(func=add_command)

    games = subcommands.add_parser("games")
    games.set_defaults(func=games_command)

    stats = subcommands.add_parser("stats")
    stats.set_defaults(func=stats_command)

    args = parser.parse_args()
    command = args.func
    delattr(args, "func")
    command(**vars(args))

if __name__ == "__main__":
    main() # pragma: no cover
