"""
Tests for the GameUseCases.
Verifies business logic for game operations.
"""

import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from entities.game import Game


class TestGameUseCases:
    """Test suite for GameUseCases."""

    def test_create_game_success(self, game_use_cases):
        """Test creating a game with valid data."""
        # Mock the repository to return None for find_by_name
        game_use_cases.game_repo.find_by_name = Mock(return_value=None)
        game_use_cases.game_repo.insert = Mock(return_value=Game(id=1, name="New Game", description="Description"))
        
        result = game_use_cases.create_game("New Game", "Description")
        
        assert result.name == "New Game"
        game_use_cases.game_repo.insert.assert_called_once()

    def test_create_game_raises_error_for_empty_name(self, game_use_cases):
        """Test that creating a game with empty name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            game_use_cases.create_game("", "Description")
        
        assert "должно быть от 1 до 100 символов" in str(exc_info.value)

    def test_create_game_raises_error_for_name_too_long(self, game_use_cases):
        """Test that creating a game with name > 100 chars raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            game_use_cases.create_game("a" * 101, "Description")
        
        assert "должно быть от 1 до 100 символов" in str(exc_info.value)

    def test_create_game_raises_error_for_duplicate_name(self, game_use_cases):
        """Test that creating a game with existing name raises ValueError."""
        existing_game = Game(id=1, name="Existing Game", description="Description")
        game_use_cases.game_repo.find_by_name = Mock(return_value=existing_game)
        
        with pytest.raises(ValueError) as exc_info:
            game_use_cases.create_game("Existing Game", "Description")
        
        assert "уже существует" in str(exc_info.value)

    def test_create_game_raises_error_for_none_name(self, game_use_cases):
        """Test that creating a game with None name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            game_use_cases.create_game(None, "Description")
        
        assert "должно быть от 1 до 100 символов" in str(exc_info.value)

    def test_get_all_games_returns_list(self, game_use_cases):
        """Test that get_all_games returns list of games."""
        games = [
            Game(id=1, name="Game 1", description="Desc 1"),
            Game(id=2, name="Game 2", description="Desc 2"),
        ]
        game_use_cases.game_repo.get_all = Mock(return_value=games)
        
        result = game_use_cases.get_all_games()
        
        assert len(result) == 2
        assert result[0].name == "Game 1"

    def test_get_all_games_returns_empty_list(self, game_use_cases):
        """Test that get_all_games returns empty list when no games."""
        game_use_cases.game_repo.get_all = Mock(return_value=[])
        
        result = game_use_cases.get_all_games()
        
        assert result == []

    def test_get_game_returns_game_when_found(self, game_use_cases):
        """Test get_game returns game when it exists."""
        game = Game(id=1, name="Test Game", description="Test")
        game_use_cases.game_repo.find_by_id = Mock(return_value=game)
        
        result = game_use_cases.get_game(1)
        
        assert result is not None
        assert result.name == "Test Game"

    def test_get_game_returns_none_when_not_found(self, game_use_cases):
        """Test get_game returns None when game doesn't exist."""
        game_use_cases.game_repo.find_by_id = Mock(return_value=None)
        
        result = game_use_cases.get_game(999)
        
        assert result is None

    def test_create_game_calls_repository_with_correct_data(self, game_use_cases):
        """Test that create_game calls insert with correct entity."""
        game_use_cases.game_repo.find_by_name = Mock(return_value=None)
        
        inserted_game = Game(id=None, name="Test Game", description="Test Desc")
        game_use_cases.game_repo.insert = Mock(return_value=inserted_game)
        
        game_use_cases.create_game("Test Game", "Test Desc")
        
        call_args = game_use_cases.game_repo.insert.call_args[0][0]
        assert call_args.name == "Test Game"
        assert call_args.description == "Test Desc"