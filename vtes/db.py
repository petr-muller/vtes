"""Database models"""

from typing import Sequence

import peewee as pw

from vtes.game import Player, Game

DATABASE = pw.SqliteDatabase(None)


class DatabaseBaseModel(pw.Model):
    """Base class to be inherited by actual models"""
    class Meta: # pylint: disable=too-few-public-methods
        """Peewee stores database in separate 'Meta' namespace"""
        database = DATABASE


class DatabaseGameModel(DatabaseBaseModel):
    """Represents a 'Game' object in the database"""
    winning_points = pw.FloatField(null=True)
    winner = pw.CharField(null=True)
    date = pw.DateField(null=True)

    @staticmethod
    def db_create(game: Game) -> 'DatabaseGameModel':
        """Given a 'Game' object, create its image in the database"""
        db_game: DatabaseGameModel = DatabaseGameModel.create(winning_points=game.winning_points,
                                                              winner=game.winner, date=game.date)
        for result in game.player_results:
            DatabasePlayerModel.create(player=result.name, deck=result.deck, game=db_game,
                                       points=result.points)

        return db_game

    def as_game(self) -> Game:
        """Returns a 'Game' object from a database object"""
        players: Sequence[Player] = [player.as_player() for player in self.players]
        return Game(players, self.winner, self.winning_points, self.date)

    @staticmethod
    def all_games() -> Sequence[Game]:
        """Return a list of all 'Game' objects"""
        games = DatabaseGameModel.select()
        return [game.as_game() for game in games]


class DatabasePlayerModel(DatabaseBaseModel):
    """Represents a 'Player' object in the database"""
    player = pw.CharField()
    deck = pw.CharField(null=True)
    game = pw.ForeignKeyField(DatabaseGameModel, backref='players')
    points = pw.IntegerField(null=True)

    def as_player(self) -> Player:
        """Returns a 'Player' object from a database object"""
        return Player(self.player, self.deck, self.points)
