"""
Pydantic-схемы для игроков.
Содержит модели для валидации входных данных и сериализации ответов API.
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class PlayerCreate(BaseModel):
    """
    Схема для создания игрока.
    """
    username: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")


class PlayerResponse(BaseModel):
    """
    Схема ответа с данными игрока.
    """
    id: int
    username: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class PlayerWithScores(BaseModel):
    """
    Схема игрока с лучшими результатами.
    """
    id: int
    username: str
    created_at: datetime
    best_scores: list[dict] = []
    
    model_config = ConfigDict(from_attributes=True)