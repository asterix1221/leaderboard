"""
Модель SQLAlchemy для таблицы игроков (players).
Маппинг доменной сущности Player на таблицу БД.
"""

from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from infrastructure.database import Base


class PlayerModel(Base):
    """
    Модель игрока для SQLAlchemy.
    Соответствует таблице 'players' в базе данных.
    """
    __tablename__ = "players"

    # Первичный ключ
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Уникальное имя игрока (до 50 символов)
    username = Column(String(50), unique=True, nullable=False)
    
    # Дата регистрации
    created_at = Column(DateTime, default=datetime.now)

    def to_dict(self):
        """
        Преобразование модели в словарь.
        
        Returns:
            Словарь с данными игрока
        """
        return {
            "id": self.id,
            "username": self.username,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }