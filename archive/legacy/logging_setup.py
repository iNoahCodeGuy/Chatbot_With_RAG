"""
Advanced logging setup for Noah's Portfolio Chatbot
Handles SQLite database initialization and JSONL file logging
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatLogger:
    """Handles dual logging to SQLite database and JSONL file"""
    
    def __init__(self, db_path: str = "chat_logs.db", jsonl_path: str = "chat_logs.jsonl"):
        self.db_path = db_path
        self.jsonl_path = jsonl_path
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize SQLite database with chat_logs table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create chat_logs table with comprehensive fields
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    page TEXT DEFAULT 'chat',
                    referrer TEXT,
                    response_time_ms INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_session_timestamp 
                ON chat_logs(session_id, timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON chat_logs(timestamp)
            """)
            
            conn.commit()
            conn.close()
            logger.info(f"✅ SQLite database initialized: {self.db_path}")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")
            raise
    
    def log_chat_event(
        self,
        session_id: str,
        question: str,
        answer: str,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        page: str = "chat",
        referrer: Optional[str] = None,
        response_time_ms: Optional[int] = None
    ) -> bool:
        """
        Log chat event to both SQLite database and JSONL file
        
        Args:
            session_id: Unique session identifier
            question: User's question
            answer: Bot's answer
            ip_address: Client IP address
            user_agent: Client user agent string
            page: Page where interaction occurred
            referrer: HTTP referrer
            response_time_ms: Response time in milliseconds
            
        Returns:
            bool: True if logging successful, False otherwise
        """
        timestamp = datetime.utcnow().isoformat()
        
        try:
            # Log to SQLite database
            self._log_to_sqlite(
                timestamp, session_id, ip_address, user_agent,
                question, answer, page, referrer, response_time_ms
            )
            
            # Log to JSONL file
            self._log_to_jsonl(
                timestamp, session_id, ip_address, user_agent,
                question, answer, page, referrer, response_time_ms
            )
            
            logger.info(f"✅ Logged chat event for session: {session_id[:8]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to log chat event: {e}")
            return False
    
    def _log_to_sqlite(
        self,
        timestamp: str,
        session_id: str,
        ip_address: Optional[str],
        user_agent: Optional[str],
        question: str,
        answer: str,
        page: str,
        referrer: Optional[str],
        response_time_ms: Optional[int]
    ) -> None:
        """Log event to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO chat_logs 
            (timestamp, session_id, ip_address, user_agent, question, answer, page, referrer, response_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, session_id, ip_address, user_agent, question, answer, page, referrer, response_time_ms))
        
        conn.commit()
        conn.close()
    
    def _log_to_jsonl(
        self,
        timestamp: str,
        session_id: str,
        ip_address: Optional[str],
        user_agent: Optional[str],
        question: str,
        answer: str,
        page: str,
        referrer: Optional[str],
        response_time_ms: Optional[int]
    ) -> None:
        """Log event to JSONL file"""
        log_entry = {
            "timestamp": timestamp,
            "session_id": session_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "question": question,
            "answer": answer,
            "page": page,
            "referrer": referrer,
            "response_time_ms": response_time_ms
        }
        
        # Append to JSONL file (create if doesn't exist)
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a specific session"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_messages,
                    MIN(timestamp) as first_message,
                    MAX(timestamp) as last_message,
                    AVG(response_time_ms) as avg_response_time
                FROM chat_logs 
                WHERE session_id = ?
            """, (session_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return {
                "session_id": session_id,
                "total_messages": result[0],
                "first_message": result[1],
                "last_message": result[2],
                "avg_response_time_ms": result[3]
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get session stats: {e}")
            return {}
    
    def get_daily_stats(self, date: str = None) -> Dict[str, Any]:
        """Get daily statistics (default: today)"""
        if not date:
            date = datetime.utcnow().strftime("%Y-%m-%d")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_messages,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    AVG(response_time_ms) as avg_response_time
                FROM chat_logs 
                WHERE DATE(timestamp) = ?
            """, (date,))
            
            result = cursor.fetchone()
            conn.close()
            
            return {
                "date": date,
                "total_messages": result[0],
                "unique_sessions": result[1],
                "avg_response_time_ms": result[2]
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get daily stats: {e}")
            return {}

# Global logger instance
chat_logger = ChatLogger()

def log_chat_event(**kwargs) -> bool:
    """Convenience function for logging chat events"""
    return chat_logger.log_chat_event(**kwargs)