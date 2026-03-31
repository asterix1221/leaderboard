"""
Tests for the Game Controller (REST API).
Verifies HTTP endpoints for game operations.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime


class TestGameController:
    """Test suite for game API endpoints."""

    def test_create_game_success(self):
        """Test successful game creation."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.game_controller.GameRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.game import Game
                mock_repo.find_by_name.return_value = None
                mock_repo.insert.return_value = Game(
                    id=1,
                    name="New Game",
                    description="Test Description"
                )
                
                client = TestClient(app)
                response = client.post(
                    "/api/games",
                    json={"name": "New Game", "description": "Test Description"}
                )
                
                assert response.status_code == 201
                data = response.json()
                assert data["name"] == "New Game"

    def test_create_game_duplicate_name(self):
        """Test that creating game with duplicate name returns 400."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.game_controller.GameRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.game import Game
                mock_repo.find_by_name.return_value = Game(
                    id=1,
                    name="Existing Game",
                    description="Description"
                )
                
                client = TestClient(app)
                response = client.post(
                    "/api/games",
                    json={"name": "Existing Game", "description": "Desc"}
                )
                
                assert response.status_code == 400

    def test_create_game_empty_name(self):
        """Test that creating game with empty name returns 422."""
        from main import app
        
        client = TestClient(app)
        response = client.post(
            "/api/games",
            json={"name": "", "description": "Desc"}
        )
        
        assert response.status_code == 422

    def test_create_game_name_too_long(self):
        """Test that creating game with name > 100 chars returns 422."""
        from main import app
        
        client = TestClient(app)
        response = client.post(
            "/api/games",
            json={"name": "a" * 101, "description": "Desc"}
        )
        
        assert response.status_code == 422

    def test_get_games(self):
        """Test getting all games."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.game_controller.GameRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                
                from entities.game import Game
                mock_repo.get_all.return_value = [
                    Game(id=1, name="Game 1", description="Desc 1"),
                    Game(id=2, name="Game 2", description="Desc 2"),
                ]
                
                client = TestClient(app)
                response = client.get("/api/games")
                
                assert response.status_code == 200
                data = response.json()
                assert len(data) == 2

    def test_get_games_empty(self):
        """Test getting all games when none exist."""
        from main import app
        
        with patch('infrastructure.database.SessionLocal') as mock_session:
            mock_db = Mock()
            mock_session.return_value = mock_db
            
            with patch('adapters.controllers.game_controller.GameRepository') as mock_repo_class:
                mock_repo = Mock()
                mock_repo_class.return_value = mock_repo
                mock_repo.get_all.return_value = []
                
                client = TestClient(app)
                response = client.get("/api/games")
                
                assert response.status_code == 200
                assert response.json() == []