"""
Tests for the PlayerUseCases.
Verifies business logic for player operations.
"""

import pytest
from unittest.mock import Mock
from datetime import datetime
from entities.player import Player


class TestPlayerUseCases:
    """Test suite for PlayerUseCases."""

    def test_register_player_success(self, player_use_cases):
        """Test registering a player with valid data."""
        player_use_cases.player_repo.find_by_username = Mock(return_value=None)
        player_use_cases.player_repo.insert = Mock(
            return_value=Player(id=1, username="newplayer", created_at=datetime.now())
        )
        
        result = player_use_cases.register_player("newplayer")
        
        assert result.username == "newplayer"
        player_use_cases.player_repo.insert.assert_called_once()

    def test_register_player_raises_error_for_empty_username(self, player_use_cases):
        """Test that registering with empty username raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            player_use_cases.register_player("")
        
        assert "должно быть от 1 до 50 символов" in str(exc_info.value)

    def test_register_player_raises_error_for_username_too_long(self, player_use_cases):
        """Test that registering with username > 50 chars raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            player_use_cases.register_player("a" * 51)
        
        assert "должно быть от 1 до 50 символов" in str(exc_info.value)

    def test_register_player_raises_error_for_duplicate_username(self, player_use_cases):
        """Test that registering with existing username raises ValueError."""
        existing_player = Player(id=1, username="existing", created_at=datetime.now())
        player_use_cases.player_repo.find_by_username = Mock(return_value=existing_player)
        
        with pytest.raises(ValueError) as exc_info:
            player_use_cases.register_player("existing")
        
        assert "уже занято" in str(exc_info.value)

    def test_register_player_raises_error_for_none_username(self, player_use_cases):
        """Test that registering with None username raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            player_use_cases.register_player(None)
        
        assert "должно быть от 1 до 50 символов" in str(exc_info.value)

    def test_get_player_returns_player_when_found(self, player_use_cases):
        """Test get_player returns player when it exists."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        player_use_cases.player_repo.find_by_id = Mock(return_value=player)
        
        result = player_use_cases.get_player(1)
        
        assert result is not None
        assert result.username == "testplayer"

    def test_get_player_returns_none_when_not_found(self, player_use_cases):
        """Test get_player returns None when player doesn't exist."""
        player_use_cases.player_repo.find_by_id = Mock(return_value=None)
        
        result = player_use_cases.get_player(999)
        
        assert result is None

    def test_get_player_by_username_returns_player_when_found(self, player_use_cases):
        """Test get_player_by_username returns player when it exists."""
        player = Player(id=1, username="testplayer", created_at=datetime.now())
        player_use_cases.player_repo.find_by_username = Mock(return_value=player)
        
        result = player_use_cases.get_player_by_username("testplayer")
        
        assert result is not None
        assert result.username == "testplayer"

    def test_get_player_by_username_returns_none_when_not_found(self, player_use_cases):
        """Test get_player_by_username returns None when player doesn't exist."""
        player_use_cases.player_repo.find_by_username = Mock(return_value=None)
        
        result = player_use_cases.get_player_by_username("nonexistent")
        
        assert result is None

    def test_get_all_players_returns_list(self, player_use_cases):
        """Test that get_all_players returns list of players."""
        players = [
            Player(id=1, username="player1", created_at=datetime.now()),
            Player(id=2, username="player2", created_at=datetime.now()),
        ]
        player_use_cases.player_repo.get_all = Mock(return_value=players)
        
        result = player_use_cases.get_all_players()
        
        assert len(result) == 2

    def test_get_all_players_returns_empty_list(self, player_use_cases):
        """Test that get_all_players returns empty list when no players."""
        player_use_cases.player_repo.get_all = Mock(return_value=[])
        
        result = player_use_cases.get_all_players()
        
        assert result == []

    def test_register_player_sets_created_at(self, player_use_cases):
        """Test that register_player sets the created_at timestamp."""
        player_use_cases.player_repo.find_by_username = Mock(return_value=None)
        
        created_time = datetime.now()
        inserted_player = Player(id=1, username="newplayer", created_at=created_time)
        player_use_cases.player_repo.insert = Mock(return_value=inserted_player)
        
        result = player_use_cases.register_player("newplayer")
        
        assert result.created_at is not None