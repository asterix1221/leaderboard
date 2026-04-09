"""
Pydantic-схемы для лидерборда.
Содержит модели для сериализации данных таблицы лидеров.
"""

from pydantic import BaseModel
from datetime import datetime


class LeaderboardEntrySchema(BaseModel):
    """
    Схема одной записи в лидерборде.
    """
    rank: int
    player_id: int
    username: str
    value: int
    achieved_at: str


class LeaderboardResponse(BaseModel):
    """
    Схема ответа с данными лидерборда.
    """
    game_id: int
    entries: list[LeaderboardEntrySchema]