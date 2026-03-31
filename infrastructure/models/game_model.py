"""
Модель SQLAlchemy для таблицы игр (games).
Маппинг доменной сущности Game на таблицу БД.
"""

from sqlalchemy import Column, Integer, String, Text
from infrastructure.database import Base


class GameModel(Base):
    """
    Модель игры для SQLAlchemy.
    Соответствует таблице 'games' в базе данных.
    """
    __tablename__ = "games"

    # Первичный ключ
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Уникальное название игры (до 100 символов)
    name = Column(String(100), unique=True, nullable=False)
    
    # Описание игры
    description = Column(Text, nullable=True)

    def to_dict(self):
        """
        Преобразование модели в словарь.
        
        Returns:
            Словарь с данными игры
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }