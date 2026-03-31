"""
Модель SQLAlchemy для таблицы результатов (scores).
Маппинг доменной сущности Score на таблицу БД.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from infrastructure.database import Base


class ScoreModel(Base):
    """
    Модель результата (очков) для SQLAlchemy.
    Соответствует таблице 'scores' в базе данных.
    """
    __tablename__ = "scores"

    # Первичный ключ
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Внешний ключ на игрока
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    
    # Внешний ключ на игру
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    
    # Количество очков
    value = Column(Integer, nullable=False)
    
    # Дата установления результата
    achieved_at = Column(DateTime, default=datetime.now)

    # Связь с игроком
    player = relationship("PlayerModel", backref="scores")
    
    # Связь с игрой
    game = relationship("GameModel", backref="scores")

    def to_dict(self):
        """
        Преобразование модели в словарь.
        
        Returns:
            Словарь с данными результата
        """
        return {
            "id": self.id,
            "player_id": self.player_id,
            "game_id": self.game_id,
            "value": self.value,
            "achieved_at": self.achieved_at.isoformat() if self.achieved_at else None
        }