"""
Контроллер игроков - REST API для работы с игроками.
Содержит эндпоинты для регистрации и получения профиля игрока.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from infrastructure import get_db, PlayerRepository
from use_cases import PlayerUseCases
from adapters.schemas import PlayerCreate, PlayerResponse

# Создание роутера
router = APIRouter(prefix="/api/players", tags=["players"])


@router.post("", response_model=PlayerResponse, status_code=201)
def register_player(player_data: PlayerCreate, db: Session = Depends(get_db)):
    """
    Зарегистрировать нового игрока.
    
    Параметры:
        player_data: Данные для регистрации игрока
        db: Сессия БД
        
    Returns:
        Созданный игрок
    """
    repo = PlayerRepository(db)
    use_case = PlayerUseCases(repo)
    
    try:
        player = use_case.register_player(player_data.username)
        return PlayerResponse(
            id=player.id,
            username=player.username,
            created_at=player.created_at
        )
    except ValueError as e:
        msg = str(e)
        if "не найден" in msg or "не найдена" in msg:
            raise HTTPException(status_code=404, detail=msg)
        raise HTTPException(status_code=400, detail=msg)


@router.get("", response_model=list[PlayerResponse])
def get_all_players(db: Session = Depends(get_db)):
    """
    Получить список всех зарегистрированных игроков.
    
    Returns:
        Список всех игроков
    """
    repo = PlayerRepository(db)
    use_case = PlayerUseCases(repo)
    players = use_case.get_all_players()
    return [
        PlayerResponse(id=p.id, username=p.username, created_at=p.created_at)
        for p in players
    ]


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Получить профиль игрока по ID.
    
    Параметры:
        player_id: Идентификатор игрока
        db: Сессия БД
        
    Returns:
        Данные игрока
    """
    repo = PlayerRepository(db)
    use_case = PlayerUseCases(repo)
    
    player = use_case.get_player(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Игрок не найден")
    
    return PlayerResponse(
        id=player.id,
        username=player.username,
        created_at=player.created_at
    )