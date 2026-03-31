"""
Pydantic-схемы для результатов.
Содержит модели для валидации входных данных и сериализации ответов API.
"""

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class ScoreCreate(BaseModel):
    """
    Схема для создания результата.
    """
    player_id: int = Field(..., description="ID игрока")
    game_id: int = Field(..., description="ID игры")
    value: int = Field(..., ge=0, description="Количество очков (неотрицательное)")


class ScoreResponse(BaseModel):
    """
    Схема ответа с данными результата.
    """
    id: int
    player_id: int
    game_id: int
    value: int
    achieved_at: datetime
    
    model_config = ConfigDict(from_attributes=True)