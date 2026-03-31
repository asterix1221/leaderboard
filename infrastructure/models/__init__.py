"""
Модели SQLAlchemy - маппинг доменных сущностей на таблицы БД.
Содержит модели PlayerModel, GameModel, ScoreModel.
"""

from infrastructure.models.player_model import PlayerModel
from infrastructure.models.game_model import GameModel
from infrastructure.models.score_model import ScoreModel

__all__ = ['PlayerModel', 'GameModel', 'ScoreModel']