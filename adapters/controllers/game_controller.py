"""
Контроллер игр - REST API для работы с играми.
Содержит эндпоинты для создания и получения списка игр.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure import get_db, GameRepository
from use_cases import GameUseCases
from adapters.schemas import GameCreate, GameResponse

# Создание роутера
router = APIRouter(prefix="/api/games", tags=["games"])


@router.post("", response_model=GameResponse, status_code=201)
def create_game(game_data: GameCreate, db: Session = Depends(get_db)):
    """
    Создать новую игру.
    
    Параметры:
        game_data: Данные для создания игры
        db: Сессия БД
        
    Возвращает:
        Созданная игра
    """
    repo = GameRepository(db)
    use_case = GameUseCases(repo)
    
    try:
        game = use_case.create_game(game_data.name, game_data.description)
        return GameResponse(
            id=game.id,
            name=game.name,
            description=game.description
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[GameResponse])
def get_games(db: Session = Depends(get_db)):
    """
    Получить список всех игр.
    
    Параметры:
        db: Сессия БД
        
    Возвращает:
        Список всех игр
    """
    repo = GameRepository(db)
    use_case = GameUseCases(repo)
    games = use_case.get_all_games()
    
    return [
        GameResponse(
            id=g.id,
            name=g.name,
            description=g.description
        )
        for g in games
    ]