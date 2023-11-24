from sqlalchemy import Column, String, ForeignKey, JSON, Integer, Enum

from game.constants import GameStatus
from models.base import AbstractDefaultModel


class Game(AbstractDefaultModel):
    __tablename__ = 'game'

    player_1 = Column(String(36), ForeignKey('users.id'))
    player_2 = Column(String(36), ForeignKey('users.id'))
    winner = Column(String(36), ForeignKey('users.id'), nullable=True)
    status = Column(Enum(GameStatus))

    player_turn = Column(String(36), ForeignKey('users.id'), nullable=True)
    board = Column(JSON(), nullable=True)


class PlayersMoves(AbstractDefaultModel):
    __tablename__ = 'player_moves'

    player = Column(String(36), ForeignKey('users.id'))
    row = Column(Integer())
    game_id = Column(String(36), ForeignKey('game.id'))
