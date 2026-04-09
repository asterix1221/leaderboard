"""
Tests for database module.
Verifies database configuration and utilities.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDatabaseModule:
    """Test suite for database module."""

    def test_database_url_format(self):
        """Test that DATABASE_URL is properly formatted."""
        from infrastructure.database import DATABASE_URL, DB_PATH
        
        assert DATABASE_URL.startswith("sqlite:///")
        assert "leaderboard.db" in str(DB_PATH)

    def test_session_local_creation(self):
        """Test that SessionLocal can be created."""
        from infrastructure.database import SessionLocal, engine
        
        # Verify SessionLocal is a sessionmaker
        assert isinstance(SessionLocal, sessionmaker)

    def test_engine_creation(self):
        """Test that engine is created properly."""
        from infrastructure.database import engine
        
        # Verify engine exists and has correct dialect
        assert engine.url.drivername == "sqlite"

    def test_get_db_generator(self):
        """Test that get_db is a generator function."""
        from infrastructure.database import get_db
        
        # get_db should be a generator
        gen = get_db()
        # Should be able to get first value (the session)
        db = next(gen)
        assert db is not None
        # Should be able to close the generator
        gen.close()

    def test_create_tables_function_exists(self):
        """Test that create_tables function exists and is callable."""
        from infrastructure.database import create_tables
        
        assert callable(create_tables)

    def test_base_declarative_exists(self):
        """Test that Base is defined."""
        from infrastructure.database import Base
        
        assert Base is not None