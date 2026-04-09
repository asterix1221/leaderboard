"""
Tests for the ScoreRepository.
Verifies database operations for scores.
"""

import pytest
from datetime import datetime
from entities.score import Score
from infrastructure.models.score_model import ScoreModel


class TestScoreRepository:
    """Test suite for ScoreRepository."""

    def test_insert_creates_score_and_returns_with_id(self, score_repository, sample_score):
        """Test that insert creates a score and returns it with an ID."""
        result = score_repository.insert(sample_score)
        
        assert result.id is not None
        assert result.id > 0
        assert result.player_id == sample_score.player_id
        assert result.game_id == sample_score.game_id
        assert result.value == sample_score.value

    def test_insert_saves_to_database(self, score_repository, db_session, db_game_and_player):
        """Test that insert actually saves to the database."""
        game, player = db_game_and_player
        score = Score(
            id=None,
            player_id=player.id,
            game_id=game.id,
            value=5000,
            achieved_at=datetime.now()
        )
        score_repository.insert(score)
        
        # Query directly from database
        db_score = db_session.query(ScoreModel).filter_by(value=5000).first()
        
        assert db_score is not None
        assert db_score.value == 5000

    def test_find_by_id_returns_score_when_exists(self, score_repository, db_session, db_game_and_player):
        """Test find_by_id returns score when it exists."""
        game, player = db_game_and_player
        score = ScoreModel(player_id=player.id, game_id=game.id, value=1000, achieved_at=datetime.now())
        db_session.add(score)
        db_session.commit()
        db_session.refresh(score)
        
        result = score_repository.find_by_id(score.id)
        
        assert result is not None
        assert result.id == score.id
        assert result.value == 1000

    def test_find_by_id_returns_none_when_not_exists(self, score_repository):
        """Test find_by_id returns None when score doesn't exist."""
        result = score_repository.find_by_id(99999)
        
        assert result is None

    def test_find_by_player_returns_all_scores_for_player(self, score_repository, db_session, db_game_and_player):
        """Test find_by_player returns all scores for a specific player."""
        game, player = db_game_and_player
        
        # Create multiple scores for the same player
        scores = [
            ScoreModel(player_id=player.id, game_id=game.id, value=1000, achieved_at=datetime.now()),
            ScoreModel(player_id=player.id, game_id=game.id, value=2000, achieved_at=datetime.now()),
            ScoreModel(player_id=player.id, game_id=game.id, value=1500, achieved_at=datetime.now()),
        ]
        db_session.add_all(scores)
        db_session.commit()
        
        result = score_repository.find_by_player(player.id)
        
        assert len(result) == 3

    def test_find_by_player_returns_empty_list_when_no_scores(self, score_repository, db_player):
        """Test find_by_player returns empty list when player has no scores."""
        result = score_repository.find_by_player(db_player.id)
        
        assert result == []

    def test_find_by_player_returns_scores_only_for_that_player(self, score_repository, db_session, db_multiple_players, db_multiple_games):
        """Test find_by_player only returns scores for the specified player."""
        player1, player2, player3 = db_multiple_players
        game1, game2, game3 = db_multiple_games
        
        # Create scores for different players
        scores = [
            ScoreModel(player_id=player1.id, game_id=game1.id, value=1000, achieved_at=datetime.now()),
            ScoreModel(player_id=player2.id, game_id=game1.id, value=2000, achieved_at=datetime.now()),
            ScoreModel(player_id=player1.id, game_id=game2.id, value=3000, achieved_at=datetime.now()),
        ]
        db_session.add_all(scores)
        db_session.commit()
        
        result = score_repository.find_by_player(player1.id)
        
        assert len(result) == 2
        for score in result:
            assert score.player_id == player1.id

    def test_get_top_scores_returns_top_scores_for_game(self, score_repository, db_session, db_multiple_players, db_multiple_games):
        """Test get_top_scores returns top scores for a game."""
        player1, player2, player3 = db_multiple_players
        game1, game2, game3 = db_multiple_games
        
        # Create scores - player1 has two scores in game1 (1000 and 2000)
        scores = [
            ScoreModel(player_id=player1.id, game_id=game1.id, value=1000, achieved_at=datetime.now()),
            ScoreModel(player_id=player1.id, game_id=game1.id, value=2000, achieved_at=datetime.now()),
            ScoreModel(player_id=player2.id, game_id=game1.id, value=1500, achieved_at=datetime.now()),
            ScoreModel(player_id=player3.id, game_id=game1.id, value=500, achieved_at=datetime.now()),
        ]
        db_session.add_all(scores)
        db_session.commit()
        
        result = score_repository.get_top_scores(game1.id, limit=10)
        
        # Should return top scores (best per player): player1=2000, player2=1500, player3=500
        assert len(result) == 3
        # First result should be player1 with 2000
        assert result[0]["value"] == 2000
        assert result[0]["username"] == "player1"

    def test_get_top_scores_respects_limit(self, score_repository, db_session, db_multiple_players, db_multiple_games):
        """Test get_top_scores respects the limit parameter."""
        player1, player2, player3 = db_multiple_players
        game1, game2, game3 = db_multiple_games
        
        scores = [
            ScoreModel(player_id=player1.id, game_id=game1.id, value=3000, achieved_at=datetime.now()),
            ScoreModel(player_id=player2.id, game_id=game1.id, value=2000, achieved_at=datetime.now()),
            ScoreModel(player_id=player3.id, game_id=game1.id, value=1000, achieved_at=datetime.now()),
        ]
        db_session.add_all(scores)
        db_session.commit()
        
        result = score_repository.get_top_scores(game1.id, limit=2)
        
        assert len(result) == 2

    def test_get_top_scores_returns_empty_when_no_scores(self, score_repository, db_game):
        """Test get_top_scores returns empty list when no scores exist."""
        result = score_repository.get_top_scores(db_game.id, limit=10)
        
        assert result == []

    def test_get_top_scores_includes_achieved_at(self, score_repository, db_session, db_game_and_player):
        """Test get_top_scores includes the achieved_at date."""
        game, player = db_game_and_player
        achieved_at = datetime(2023, 1, 15, 10, 0, 0)
        score = ScoreModel(player_id=player.id, game_id=game.id, value=1000, achieved_at=achieved_at)
        db_session.add(score)
        db_session.commit()
        db_session.refresh(score)
        
        result = score_repository.get_top_scores(game.id, limit=10)
        
        assert len(result) == 1
        assert result[0]["achieved_at"] is not None

    def test_insert_after_insert_has_correct_id(self, score_repository, db_session, db_game_and_player):
        """Test that the ID assigned by insert can be used to find the score."""
        game, player = db_game_and_player
        score = Score(id=None, player_id=player.id, game_id=game.id, value=1000, achieved_at=datetime.now())
        
        inserted_score = score_repository.insert(score)
        found_score = score_repository.find_by_id(inserted_score.id)
        
        assert found_score is not None
        assert found_score.id == inserted_score.id