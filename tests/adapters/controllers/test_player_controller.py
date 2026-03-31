"""
Tests for the Player Controller (REST API).
Verifies HTTP endpoints for player operations.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime


class TestPlayerController:
    """Test suite for player API endpoints."""

    def test_register_player_success(self):
        """Test successful player registration."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.player_controller.PlayerRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.player import Player
                mock_repo.find_by_username.return_value = None
                mock_repo.insert.return_value = Player(
                    id=1,
                    username="newplayer",
                    created_at=datetime.now()
                )
                
                client = TestClient(app)
                response = client.post("/api/players", json={"username": "newplayer"})
                
                assert response.status_code == 201
                data = response.json()
                assert data["username"] == "newplayer"
                assert data["id"] == 1

    def test_register_player_duplicate_username(self):
        """Test that registering duplicate username returns 400."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.player_controller.PlayerRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.player import Player
                mock_repo.find_by_username.return_value = Player(
                    id=1,
                    username="existing",
                    created_at=datetime.now()
                )
                
                client = TestClient(app)
                response = client.post("/api/players", json={"username": "existing"})
                
                assert response.status_code == 400

    def test_register_player_empty_username(self):
        """Test that registering empty username returns 400."""
        from main import app
        
        client = TestClient(app)
        response = client.post("/api/players", json={"username": ""})
        
        assert response.status_code == 422  # Pydantic validation error

    def test_register_player_username_too_long(self):
        """Test that registering too long username returns 422."""
        from main import app
        
        client = TestClient(app)
        response = client.post("/api/players", json={"username": "a" * 51})
        
        assert response.status_code == 422

    def test_get_all_players(self):
        """Test getting all players."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.player_controller.PlayerRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.player import Player
                mock_repo.get_all.return_value = [
                    Player(id=1, username="player1", created_at=datetime.now()),
                    Player(id=2, username="player2", created_at=datetime.now()),
                ]
                
                client = TestClient(app)
                response = client.get("/api/players")
                
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2

    def test_get_all_players_empty(self):
        """Test getting all players when none exist."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.player_controller.PlayerRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                mock_repo.get_all.return_value = []
                
                client = TestClient(app)
                response = client.get("/api/players")
                
                assert response.status_code == 200
                assert response.json() == []

    def test_get_player_success(self):
        """Test getting a specific player."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.player_controller.PlayerRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.player import Player
                mock_repo.find_by_id.return_value = Player(
                    id=1,
                    username="testplayer",
                    created_at=datetime.now()
                )
                
                client = TestClient(app)
                response = client.get("/api/players/1")
                
                assert response.status_code == 200
                data = response.json()
                assert data["username"] == "testplayer"

    def test_get_player_not_found(self):
        """Test getting non-existent player returns 404."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.player_controller.PlayerRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                mock_repo.find_by_id.return_value = None
                
                client = TestClient(app)
                response = client.get("/api/players/999")
                
                assert response.status_code == 404