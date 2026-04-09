"""
Сущность игры (Game).
Бизнес-объект, представляющий игру в системе лидербордов.
Не зависит от фреймворка и базы данных.
"""

from dataclasses import dataclass


@dataclass
class Game:
    """
    Доменная модель игры.
    
    Атрибуты:
        id: Уникальный идентификатор игры (None до сохранения в БД)
        name: Название игры
        description: Краткое описание игры
    """
    id: int | None
    name: str
    description: str

    def is_valid(self) -> bool:
        """
        Проверить валидность игры.
        
        Бизнес-правило: название игры не может быть пустым.
        
        Returns:
            True если игра валидна, иначе False
        """
        return bool(self.name)