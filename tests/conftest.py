"""
Pytest configuration and fixtures for the Game Leaderboard System.
Provides testing utilities for all layers of the application.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Import entities
from entities.game import Game
from entities.player import Player
from entities.score import Score

# Import infrastructure models
from infrastructure.database import Base
from infrastructure.models.game_model import GameModel
from infrastructure.models.player_model import PlayerModel
from infrastructure.models.score_model import ScoreModel

# Import repositories
from infrastructure.repositories.game_repository import GameRepository
from infrastructure.repositories.player_repository import PlayerRepository
from infrastructure.repositories.score_repository import ScoreRepository


@pytest.fixture
def engine():
    """
    Create an in-memory SQLite engine for testing.
    This avoids file I/O and ensures test isolation.
    """
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine):
    """
    Create a database session for testing.
    Automatically creates tables before each test and cleans up after.
    """
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def game_repository(db_session):
    """Create a GameRepository instance with test session."""
    return GameRepository(db_session)


@pytest.fixture
def player_repository(db_session):
    """Create a PlayerRepository instance with test session."""
    return PlayerRepository(db_session)


@pytest.fixture
def score_repository(db_session):
    """Create a ScoreRepository instance with test session."""
    return ScoreRepository(db_session)


@pytest.fixture
def sample_game():
    """Create a sample Game entity for testing."""
    return Game(id=None, name="Test Game", description="Test Description")


@pytest.fixture
def sample_player():
    """Create a sample Player entity for testing."""
    return Player(
        id=None,
        username="testplayer",
        created_at=datetime.now()
    )


@pytest.fixture
def sample_score():
    """Create a sample Score entity for testing."""
    return Score(
        id=None,
        player_id=1,
        game_id=1,
        value=1000,
        achieved_at=datetime.now()
    )


@pytest.fixture
def db_game(db_session):
    """Create a game in the database for testing."""
    game = GameModel(name="Test Game", description="Test Description")
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    return game


@pytest.fixture
def db_player(db_session):
    """Create a player in the database for testing."""
    player = PlayerModel(username="testplayer", created_at=datetime.now())
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)
    return player


@pytest.fixture
def db_game_and_player(db_session):
    """Create both a game and player in the database for testing."""
    game = GameModel(name="Test Game", description="Test Description")
    db_session.add(game)
    db_session.commit()
    db_session.refresh(game)
    
    player = PlayerModel(username="testplayer", created_at=datetime.now())
    db_session.add(player)
    db_session.commit()
    db_session.refresh(player)
    
    return game, player


@pytest.fixture
def db_multiple_players(db_session):
    """Create multiple players in the database for testing."""
    players = [
        PlayerModel(username="player1", created_at=datetime.now()),
        PlayerModel(username="player2", created_at=datetime.now()),
        PlayerModel(username="player3", created_at=datetime.now()),
    ]
    db_session.add_all(players)
    db_session.commit()
    for player in players:
        db_session.refresh(player)
    return players


@pytest.fixture
def db_multiple_games(db_session):
    """Create multiple games in the database for testing."""
    games = [
        GameModel(name="Game 1", description="Description 1"),
        GameModel(name="Game 2", description="Description 2"),
        GameModel(name="Game 3", description="Description 3"),
    ]
    db_session.add_all(games)
    db_session.commit()
    for game in games:
        db_session.refresh(game)
    return games


@pytest.fixture
def db_multiple_scores(db_session, db_multiple_players, db_multiple_games):
    """Create multiple scores in the database for testing."""
    scores = []
    # Create scores for different players in different games
    for i, player in enumerate(db_multiple_players):
        for j, game in enumerate(db_multiple_games):
            score = ScoreModel(
                player_id=player.id,
                game_id=game.id,
                value=1000 + (i * 100) + (j * 10),
                achieved_at=datetime.now()
            )
            scores.append(score)
    
    db_session.add_all(scores)
    db_session.commit()
    for score in scores:
        db_session.refresh(score)
    return scores


# Import use cases for fixtures
@pytest.fixture
def game_use_cases(game_repository):
    """Create GameUseCases with test repository."""
    from use_cases.game_use_cases import GameUseCases
    return GameUseCases(game_repository)


@pytest.fixture
def player_use_cases(player_repository):
    """Create PlayerUseCases with test repository."""
    from use_cases.player_use_cases import PlayerUseCases
    return PlayerUseCases(player_repository)


@pytest.fixture
def score_use_cases(score_repository, player_repository, game_repository):
    """Create ScoreUseCases with test repositories."""
    from use_cases.score_use_cases import ScoreUseCases
    return ScoreUseCases(score_repository, player_repository, game_repository)


@pytest.fixture
def leaderboard_use_cases(score_repository, game_repository):
    """Create LeaderboardUseCases with test repositories."""
    from use_cases.leaderboard_use_cases import LeaderboardUseCases
    return LeaderboardUseCases(score_repository, game_repository)