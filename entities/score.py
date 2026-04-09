"""
Сущность результата (Score).
Бизнес-объект, представляющий очки игрока в конкретной игре.
Не зависит от фреймворка и базы данных.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Score:
    """
    Доменная модель результата (очков).
    
    Атрибуты:
        id: Уникальный идентификатор результата (None до сохранения в БД)
        player_id: Идентификатор игрока
        game_id: Идентификатор игры
        value: Количество очков
        achieved_at: Дата и время установления результата
    """
    id: int | None
    player_id: int
    game_id: int
    value: int
    achieved_at: datetime

    def is_valid(self) -> bool:
        """
        Проверить валидность результата.
        
        Бизнес-правило: очки не могут быть отрицательными.
        
        Returns:
            True если результат валиден, иначе False
        """
        return self.value >= 0