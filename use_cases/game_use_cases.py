"""
Сценарии использования для работы с играми.
Содержит бизнес-логику создания и получения игр.
"""

from entities.game import Game
from infrastructure.repositories import GameRepositoryProtocol


class GameUseCases:
    """
    Сценарии использования для работы с играми.
    Реализует бизнес-логику, связанную с играми.
    """

    def __init__(self, game_repo: GameRepositoryProtocol):
        # Внедрение зависимости через конструктор
        self.game_repo = game_repo

    def create_game(self, name: str, description: str) -> Game:
        """
        Создать новую игру.

        Правила:
        - Название не может быть пустым
        - Название должно быть уникальным

        Args:
            name: Название игры
            description: Описание игры

        Returns:
            Созданная игра

        Raises:
            ValueError: Если название пустое или уже занято
        """
        # Проверка валидности названия
        if not name or len(name) > 100:
            raise ValueError("Название игры должно быть от 1 до 100 символов")

        # Проверка уникальности названия
        existing = self.game_repo.find_by_name(name)
        if existing:
            raise ValueError("Игра с таким названием уже существует")

        # Создание игры через доменную сущность
        game = Game(id=None, name=name, description=description)
        return self.game_repo.insert(game)

    def get_all_games(self) -> list[Game]:
        """
        Получить список всех игр.

        Returns:
            Список всех игр
        """
        return self.game_repo.get_all()

    def get_game(self, game_id: int) -> Game | None:
        """
        Получить игру по ID.

        Args:
            game_id: Идентификатор игры

        Returns:
            Игра или None
        """
        return self.game_repo.find_by_id(game_id)
