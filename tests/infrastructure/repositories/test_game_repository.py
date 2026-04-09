"""
Tests for the GameRepository.
Verifies database operations for games.
"""

import pytest
from datetime import datetime
from entities.game import Game


class TestGameRepository:
    """Test suite for GameRepository."""

    def test_insert_creates_game_and_returns_with_id(self, game_repository, sample_game):
        """Test that insert creates a game and returns it with an ID."""
        result = game_repository.insert(sample_game)
        
        assert result.id is not None
        assert result.id > 0
        assert result.name == sample_game.name
        assert result.description == sample_game.description

    def test_insert_saves_to_database(self, game_repository, db_session):
        """Test that insert actually saves to the database."""
        game = Game(id=None, name="New Game", description="Description")
        game_repository.insert(game)
        
        # Query directly from database
        db_game = db_session.query(
            __import__('infrastructure.models.game_model', fromlist=['GameModel']).GameModel
        ).filter_by(name="New Game").first()
        
        assert db_game is not None
        assert db_game.name == "New Game"

    def test_find_by_id_returns_game_when_exists(self, game_repository, db_game):
        """Test find_by_id returns game when it exists."""
        result = game_repository.find_by_id(db_game.id)
        
        assert result is not None
        assert result.id == db_game.id
        assert result.name == db_game.name

    def test_find_by_id_returns_none_when_not_exists(self, game_repository):
        """Test find_by_id returns None when game doesn't exist."""
        result = game_repository.find_by_id(99999)
        
        assert result is None

    def test_find_by_name_returns_game_when_exists(self, game_repository, db_game):
        """Test find_by_name returns game when it exists."""
        result = game_repository.find_by_name(db_game.name)
        
        assert result is not None
        assert result.name == db_game.name
        assert result.description == db_game.description

    def test_find_by_name_returns_none_when_not_exists(self, game_repository):
        """Test find_by_name returns None when game doesn't exist."""
        result = game_repository.find_by_name("NonExistentGame")
        
        assert result is None

    def test_get_all_returns_all_games(self, game_repository, db_multiple_games):
        """Test get_all returns all games."""
        result = game_repository.get_all()
        
        assert len(result) == 3
        names = [g.name for g in result]
        assert "Game 1" in names
        assert "Game 2" in names
        assert "Game 3" in names

    def test_get_all_returns_empty_list_when_no_games(self, game_repository):
        """Test get_all returns empty list when no games exist."""
        result = game_repository.get_all()
        
        assert result == []

    def test_insert_creates_game_with_unicode_name(self, game_repository):
        """Test inserting game with unicode characters."""
        game = Game(id=None, name="Космический шутер", description="Игра")
        result = game_repository.insert(game)
        
        assert result.name == "Космический шутер"

    def test_find_by_id_after_insert_has_correct_id(self, game_repository):
        """Test that the ID assigned by insert can be used to find the game."""
        game = Game(id=None, name="Test Game", description="Test")
        inserted_game = game_repository.insert(game)
        
        found_game = game_repository.find_by_id(inserted_game.id)
        
        assert found_game is not None
        assert found_game.id == inserted_game.id