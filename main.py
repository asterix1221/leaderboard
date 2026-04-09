"""
Точка входа в приложение Game Leaderboard System.
Настраивает FastAPI, подключает роутеры, CORS и статические файлы.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    """
    print("Создание таблиц базы данных...")
    create_tables()
    print("Таблицы созданы")
    
    # Заполнение тестовыми данными
    seed_data()
    
    yield

# Импорт функции создания таблиц и подключения к БД
from infrastructure.database import create_tables, SessionLocal
from infrastructure import PlayerModel, GameModel, ScoreModel

# Импорт роутеров контроллеров
from adapters.controllers.player_controller import router as player_router
from adapters.controllers.game_controller import router as game_router
from adapters.controllers.score_controller import router as score_router
from adapters.controllers.leaderboard_controller import router as leaderboard_router

# Создание приложения FastAPI
app = FastAPI(
    title="Game Leaderboard System",
    description="Серверная часть системы лидербордов для игры",
    version="1.0.0",
    lifespan=lifespan
)

# Настройка CORS (разрешить все источники для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(player_router)
app.include_router(game_router)
app.include_router(score_router)
app.include_router(leaderboard_router)

# Монтирование статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """
    Перенаправление корневого URL на статический HTML.
    """
    return RedirectResponse(url="/static/index.html")


def seed_data():
    """
    Заполнение базы данных тестовыми данными.
    Создает игры, игроков и результаты для демонстрации лидерборда.
    """
    db = SessionLocal()
    
    try:
        # Проверка, пустая ли база
        if db.query(GameModel).first() is not None:
            print("База данных уже содержит данные, пропускаем заполнение")
            return
        
        print("Заполнение базы данных тестовыми данными...")
        
        # Создание игр
        games = [
            GameModel(name="Space Shooter", description="Космический шутер"),
            GameModel(name="Puzzle Master", description="Головоломки"),
            GameModel(name="Racing Pro", description="Гонки")
        ]
        db.add_all(games)
        db.commit()
        
        # Обновляем ID после сохранения
        for game in games:
            db.refresh(game)
        
        # Создание игроков
        players = []
        for i in range(1, 6):
            player = PlayerModel(
                username=f"player{i}",
                created_at=datetime.now()
            )
            players.append(player)
        
        db.add_all(players)
        db.commit()
        
        # Обновляем ID после сохранения
        for player in players:
            db.refresh(player)
        
        # Создание результатов (15-20 случайных результатов)
        score_count = 0
        for _ in range(20):
            player = random.choice(players)
            game = random.choice(games)
            value = random.randint(100, 5000)
            
            # Проверяем, есть ли уже результат для этого игрока и игры
            existing = db.query(ScoreModel).filter(
                ScoreModel.player_id == player.id,
                ScoreModel.game_id == game.id
            ).first()
            
            if not existing:
                score = ScoreModel(
                    player_id=player.id,
                    game_id=game.id,
                    value=value,
                    achieved_at=datetime.now()
                )
                db.add(score)
                score_count += 1
        
        db.commit()
        print(f"Создано {score_count} результатов")
        print("Тестовые данные успешно загружены")
        
    except Exception as e:
        print(f"Ошибка при заполнении данных: {e}")
        db.rollback()
    finally:
        db.close()



# Запуск: uvicorn main:app --reload --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)