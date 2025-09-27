"""
Analytics Service
================

Handles user interaction tracking, question analytics, and usage statistics.
Clean architecture with proper data models and error handling.
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


@dataclass
class UserInteraction:
    """Data model for user interactions."""
    session_id: str
    user_type: str
    question: str
    answer: str
    timestamp: datetime
    response_time: float
    user_rating: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "user_type": self.user_type,
            "question": self.question,
            "answer": self.answer,
            "timestamp": self.timestamp.isoformat(),
            "response_time": self.response_time,
            "user_rating": self.user_rating
        }


@dataclass
class AnalyticsStats:
    """Analytics statistics data model."""
    total_questions: int
    unique_users: int
    avg_response_time: float
    popular_questions: List[Dict[str, Any]]
    user_type_distribution: Dict[str, int]
    daily_usage: List[Dict[str, Any]]


class DatabaseManager:
    """Manages SQLite database operations for analytics.
    
    Handles connection management, schema creation, and data persistence
    with proper error handling and connection pooling.
    """
    
    def __init__(self, db_path: str = "data/analytics.db"):
        """Initialize database manager.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self) -> None:
        """Create database and tables if they don't exist."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
        
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    user_type TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    response_time REAL NOT NULL,
                    user_rating INTEGER
                )
            """)
            
            # Create indices for better query performance
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_id 
                ON user_interactions(session_id)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON user_interactions(timestamp)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_type 
                ON user_interactions(user_type)
            """)
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get database connection with proper configuration.
        
        Returns:
            sqlite3.Connection: Configured database connection
        """
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access to rows
        return conn
    
    def save_interaction(self, interaction: UserInteraction) -> None:
        """Save user interaction to database.
        
        Args:
            interaction: User interaction to save
            
        Raises:
            RuntimeError: If database operation fails
        """
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO user_interactions 
                    (session_id, user_type, question, answer, timestamp, response_time, user_rating)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    interaction.session_id,
                    interaction.user_type,
                    interaction.question,
                    interaction.answer,
                    interaction.timestamp.isoformat(),
                    interaction.response_time,
                    interaction.user_rating
                ))
                logger.debug(f"Saved interaction for session {interaction.session_id}")
                
        except Exception as e:
            logger.error(f"Failed to save interaction: {e}")
            raise RuntimeError(f"Database save failed: {str(e)}")
    
    def get_analytics_data(self, days: int = 30) -> AnalyticsStats:
        """Get analytics statistics for specified period.
        
        Args:
            days: Number of days to include in statistics
            
        Returns:
            AnalyticsStats: Computed analytics statistics
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            with self._get_connection() as conn:
                # Get basic stats
                total_questions = conn.execute(
                    "SELECT COUNT(*) as count FROM user_interactions WHERE timestamp >= ?",
                    (cutoff_date,)
                ).fetchone()["count"]
                
                unique_users = conn.execute(
                    "SELECT COUNT(DISTINCT session_id) as count FROM user_interactions WHERE timestamp >= ?",
                    (cutoff_date,)
                ).fetchone()["count"]
                
                avg_response_time = conn.execute(
                    "SELECT AVG(response_time) as avg FROM user_interactions WHERE timestamp >= ?",
                    (cutoff_date,)
                ).fetchone()["avg"] or 0.0
                
                # Get popular questions
                popular_questions = conn.execute("""
                    SELECT question, COUNT(*) as count 
                    FROM user_interactions 
                    WHERE timestamp >= ?
                    GROUP BY question 
                    ORDER BY count DESC 
                    LIMIT 10
                """, (cutoff_date,)).fetchall()
                
                # Get user type distribution
                user_type_dist = conn.execute("""
                    SELECT user_type, COUNT(*) as count 
                    FROM user_interactions 
                    WHERE timestamp >= ?
                    GROUP BY user_type
                """, (cutoff_date,)).fetchall()
                
                # Get daily usage
                daily_usage = conn.execute("""
                    SELECT DATE(timestamp) as date, COUNT(*) as count
                    FROM user_interactions 
                    WHERE timestamp >= ?
                    GROUP BY DATE(timestamp)
                    ORDER BY date DESC
                    LIMIT 30
                """, (cutoff_date,)).fetchall()
                
                return AnalyticsStats(
                    total_questions=total_questions,
                    unique_users=unique_users,
                    avg_response_time=avg_response_time,
                    popular_questions=[dict(row) for row in popular_questions],
                    user_type_distribution={row["user_type"]: row["count"] for row in user_type_dist},
                    daily_usage=[dict(row) for row in daily_usage]
                )
                
        except Exception as e:
            logger.error(f"Failed to get analytics data: {e}")
            raise RuntimeError(f"Analytics query failed: {str(e)}")


class AnalyticsService:
    """Main analytics service providing high-level analytics operations.
    
    Orchestrates data collection, storage, and analysis with clean interfaces
    and proper error handling.
    """
    
    def __init__(self, db_path: str = "data/analytics.db"):
        """Initialize analytics service.
        
        Args:
            db_path: Path to analytics database
        """
        self.db_manager = DatabaseManager(db_path)
    
    def track_question(
        self, 
        session_id: str,
        user_type: str,
        question: str,
        answer: str,
        response_time: float,
        user_rating: Optional[int] = None
    ) -> None:
        """Track a user question and response.
        
        Args:
            session_id: Unique session identifier
            user_type: Type of user (e.g., "Hiring Manager")
            question: User's question
            answer: AI's response
            response_time: Time taken to generate response
            user_rating: Optional user rating (1-5)
        """
        interaction = UserInteraction(
            session_id=session_id,
            user_type=user_type,
            question=question,
            answer=answer,
            timestamp=datetime.now(),
            response_time=response_time,
            user_rating=user_rating
        )
        
        self.db_manager.save_interaction(interaction)
    
    def get_stats(self, days: int = 30) -> AnalyticsStats:
        """Get analytics statistics.
        
        Args:
            days: Number of days to include in analysis
            
        Returns:
            AnalyticsStats: Analytics statistics
        """
        return self.db_manager.get_analytics_data(days)
    
    def export_data(self, format: str = "json") -> str:
        """Export analytics data for external analysis.
        
        Args:
            format: Export format ("json" or "csv")
            
        Returns:
            str: Exported data as string
            
        Raises:
            ValueError: If format is not supported
        """
        if format not in ["json", "csv"]:
            raise ValueError(f"Unsupported export format: {format}")
        
        stats = self.get_stats(days=365)  # Get full year of data
        
        if format == "json":
            return json.dumps(asdict(stats), indent=2, default=str)
        
        # CSV export would be implemented here if needed
        raise NotImplementedError("CSV export not yet implemented")


# Singleton instance for application use
_analytics_service: Optional[AnalyticsService] = None


def get_analytics_service() -> AnalyticsService:
    """Get global analytics service instance (singleton pattern).
    
    Returns:
        AnalyticsService: Analytics service instance
    """
    global _analytics_service
    
    if _analytics_service is None:
        _analytics_service = AnalyticsService()
    
    return _analytics_service