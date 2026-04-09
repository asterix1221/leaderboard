"""
Pydantic-схемы для игр.
Содержит модели для валидации входных данных и сериализации ответов API.
"""

from pydantic import BaseModel, ConfigDict, Field


class GameCreate(BaseModel):
    """
    Схема для создания игры.
    """
    name: str = Field(..., min_length=1, max_length=100, description="Название игры")
    description: str = Field(default="", description="Описание игры")


class GameResponse(BaseModel):
    """
    Схема ответа с данными игры.
    """
    id: int
    name: str
    description: str
    
    model_config = ConfigDict(from_attributes=True)