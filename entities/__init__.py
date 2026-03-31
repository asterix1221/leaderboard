"""
Слой Entities (Сущности) - бизнес-объекты, не зависящие от фреймворков и БД.
Содержит доменные модели: Player, Score, Game.
"""

from entities.player import Player
from entities.score import Score
from entities.game import Game

__all__ = ['Player', 'Score', 'Game']