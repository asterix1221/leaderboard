"""
Tests for the PlayerRepository.
Verifies database operations for players.
"""

import pytest
from datetime import datetime
from entities.player import Player


class TestPlayerRepository:
    """Test suite for PlayerRepository."""

    def test_insert_creates_player_and_returns_with_id(self, player_repository, sample_player):
        """Test that insert creates a player and returns it with an ID."""
        result = player_repository.insert(sample_player)
        
        assert result.id is not None
        assert result.id > 0
        assert result.username == sample_player.username

    def test_insert_saves_to_database(self, player_repository, db_session):
        """Test that insert actually saves to the database."""
        from infrastructure.models.player_model import PlayerModel
        
        player = Player(id=None, username="newplayer", created_at=datetime.now())
        player_repository.insert(player)
        
        # Query directly from database
        db_player = db_session.query(PlayerModel).filter_by(username="newplayer").first()
        
        assert db_player is not None
        assert db_player.username == "newplayer"

    def test_find_by_id_returns_player_when_exists(self, player_repository, db_player):
        """Test find_by_id returns player when it exists."""
        result = player_repository.find_by_id(db_player.id)
        
        assert result is not None
        assert result.id == db_player.id
        assert result.username == db_player.username

    def test_find_by_id_returns_none_when_not_exists(self, player_repository):
        """Test find_by_id returns None when player doesn't exist."""
        result = player_repository.find_by_id(99999)
        
        assert result is None

    def test_find_by_username_returns_player_when_exists(self, player_repository, db_player):
        """Test find_by_username returns player when it exists."""
        result = player_repository.find_by_username(db_player.username)
        
        assert result is not None
        assert result.username == db_player.username

    def test_find_by_username_returns_none_when_not_exists(self, player_repository):
        """Test find_by_username returns None when player doesn't exist."""
        result = player_repository.find_by_username("NonExistentPlayer")
        
        assert result is None

    def test_get_all_returns_all_players(self, player_repository, db_multiple_players):
        """Test get_all returns all players."""
        result = player_repository.get_all()
        
        assert len(result) == 3
        usernames = [p.username for p in result]
        assert "player1" in usernames
        assert "player2" in usernames
        assert "player3" in usernames

    def test_get_all_returns_empty_list_when_no_players(self, player_repository):
        """Test get_all returns empty list when no players exist."""
        result = player_repository.get_all()
        
        assert result == []

    def test_insert_preserves_created_at(self, player_repository):
        """Test that insert preserves the created_at timestamp."""
        created_at = datetime(2023, 1, 15, 10, 30, 0)
        player = Player(id=None, username="testplayer", created_at=created_at)
        
        result = player_repository.insert(player)
        
        assert result.created_at == created_at

    def test_find_by_id_after_insert_has_correct_id(self, player_repository):
        """Test that the ID assigned by insert can be used to find the player."""
        player = Player(id=None, username="testplayer", created_at=datetime.now())
        inserted_player = player_repository.insert(player)
        
        found_player = player_repository.find_by_id(inserted_player.id)
        
        assert found_player is not None
        assert found_player.id == inserted_player.id

    def test_find_by_username_is_case_sensitive(self, player_repository, db_player):
        """Test that username search is case sensitive."""
        # Assuming db_player has username "testplayer"
        result = player_repository.find_by_username("TestPlayer")
        
        assert result is None