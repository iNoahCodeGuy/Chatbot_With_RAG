"""SQLite-based analytics system for tracking chatbot interactions."""
import sqlite3
import json
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from collections import Counter

class ChatbotAnalytics:
    def __init__(self, db_path: str = "chatbot_analytics.db"):
        """Initialize analytics database."""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create the analytics table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS question_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    source_count INTEGER,
                    response_time_ms REAL,
                    linkedin_included BOOLEAN DEFAULT FALSE,
                    is_career_related BOOLEAN DEFAULT FALSE,
                    metadata TEXT,
                    session_id TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON question_analytics(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_career_related 
                ON question_analytics(is_career_related)
            """)
            
            conn.commit()
    
    def log_interaction(self, 
                       question: str, 
                       answer: str, 
                       source_count: int = 0,
                       response_time_ms: Optional[float] = None,
                       linkedin_included: bool = False,
                       is_career_related: bool = False,
                       metadata: Optional[Dict] = None,
                       session_id: Optional[str] = None) -> int:
        """
        Log a chatbot interaction to the database.
        
        Args:
            question: The user's question
            answer: The chatbot's response
            source_count: Number of source documents used
            response_time_ms: Time taken to generate response in milliseconds
            linkedin_included: Whether LinkedIn URL was included in response
            is_career_related: Whether question was career-related
            metadata: Additional data as dictionary
            session_id: Session identifier for grouping interactions
            
        Returns:
            int: The ID of the logged interaction
        """
        timestamp = datetime.now().isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO question_analytics 
                (timestamp, question, answer, source_count, response_time_ms, 
                 linkedin_included, is_career_related, metadata, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, question, answer, source_count, response_time_ms,
                linkedin_included, is_career_related, 
                json.dumps(metadata) if metadata else None,
                session_id
            ))
            
            interaction_id = cursor.lastrowid
            conn.commit()
            
        return interaction_id
    
    def get_analytics_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics summary for the last N days."""
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total interactions
            cursor.execute("""
                SELECT COUNT(*) FROM question_analytics 
                WHERE timestamp >= ?
            """, (cutoff_date,))
            total_interactions = cursor.fetchone()[0]
            
            # Career-related questions
            cursor.execute("""
                SELECT COUNT(*) FROM question_analytics 
                WHERE timestamp >= ? AND is_career_related = TRUE
            """, (cutoff_date,))
            career_questions = cursor.fetchone()[0]
            
            # LinkedIn inclusions
            cursor.execute("""
                SELECT COUNT(*) FROM question_analytics 
                WHERE timestamp >= ? AND linkedin_included = TRUE
            """, (cutoff_date,))
            linkedin_inclusions = cursor.fetchone()[0]
            
            # Average response time
            cursor.execute("""
                SELECT AVG(response_time_ms) FROM question_analytics 
                WHERE timestamp >= ? AND response_time_ms IS NOT NULL
            """, (cutoff_date,))
            avg_response_time = cursor.fetchone()[0]
            
            # Fetch questions and compute common patterns in Python (first 3 words)
            cursor.execute(
                """
                SELECT question FROM question_analytics 
                WHERE timestamp >= ?
                """,
                (cutoff_date,)
            )
            questions = [row[0] for row in cursor.fetchall()]
        
        counter: Counter[str] = Counter()
        for q in questions:
            if not q:
                continue
            first_three = " ".join(q.strip().split()[:3]).lower()
            if first_three:
                counter[first_three] += 1
        common_patterns = counter.most_common(5)
            
        return {
            "period_days": days,
            "total_interactions": total_interactions,
            "career_questions": career_questions,
            "linkedin_inclusions": linkedin_inclusions,
            "avg_response_time_ms": round(avg_response_time, 2) if avg_response_time else None,
            "career_question_rate": round(career_questions / total_interactions * 100, 1) if total_interactions > 0 else 0,
            "linkedin_inclusion_rate": round(linkedin_inclusions / total_interactions * 100, 1) if total_interactions > 0 else 0,
            "common_question_patterns": common_patterns
        }
    
    def get_recent_interactions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent interactions."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, timestamp, question, answer, source_count, 
                       response_time_ms, linkedin_included, is_career_related
                FROM question_analytics 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def export_data(self, output_file: str, days: int = None):
        """Export analytics data to CSV."""
        import csv
        
        where_clause = ""
        params: List[Any] = []
        
        if days:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            where_clause = "WHERE timestamp >= ?"
            params.append(cutoff_date)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(f"""
                SELECT * FROM question_analytics 
                {where_clause}
                ORDER BY timestamp DESC
            """, params)
            
            rows = cursor.fetchall()
            
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            if rows:
                writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
                writer.writeheader()
                for row in rows:
                    writer.writerow(dict(row))
        
        return len(rows)
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get basic database statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM question_analytics")
            total_records = cursor.fetchone()[0]
            
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM question_analytics")
            date_range = cursor.fetchone()
            
            # Database file size
            db_size_mb = os.path.getsize(self.db_path) / (1024 * 1024) if os.path.exists(self.db_path) else 0
            
        return {
            "total_records": total_records,
            "date_range": {
                "earliest": date_range[0],
                "latest": date_range[1]
            },
            "database_size_mb": round(db_size_mb, 2),
            "database_path": self.db_path
        }


# Utility function for easy integration
def create_analytics_instance(db_path: str = "chatbot_analytics.db") -> ChatbotAnalytics:
    """Create and return a ChatbotAnalytics instance."""
    return ChatbotAnalytics(db_path)


# Example usage and testing
if __name__ == "__main__":
    # Demo usage
    analytics = ChatbotAnalytics("test_analytics.db")
    
    # Log a sample interaction
    interaction_id = analytics.log_interaction(
        question="What is Noah's background?",
        answer="Noah has experience in sales and AI development...",
        source_count=3,
        response_time_ms=1250.5,
        linkedin_included=True,
        is_career_related=True,
        metadata={"model": "gpt-4", "version": "1.0"}
    )
    
    print(f"Logged interaction with ID: {interaction_id}")
    
    # Get summary
    summary = analytics.get_analytics_summary(days=30)
    print(f"Analytics Summary: {summary}")
    
    # Get recent interactions
    recent = analytics.get_recent_interactions(limit=5)
    print(f"Recent interactions: {len(recent)}")
    
    # Database stats
    stats = analytics.get_database_stats()
    print(f"Database stats: {stats}")
