"""
File Storage Manager
==================

Handles file-based storage for messages, confessions, and other user data.
Simple, reliable storage with proper error handling and directory management.
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)


class FileStorageManager:
    """Manages file-based storage for user data.
    
    Provides simple, reliable storage for messages and confessions
    with proper error handling and directory management.
    """
    
    def __init__(self, base_dir: str = "data"):
        """Initialize storage manager.
        
        Args:
            base_dir: Base directory for data storage
        """
        self.base_dir = Path(base_dir)
        self._ensure_directories_exist()
    
    def _ensure_directories_exist(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.base_dir / "messages",
            self.base_dir / "confessions"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _generate_filename(self, prefix: str, timestamp: datetime) -> str:
        """Generate unique filename with timestamp.
        
        Args:
            prefix: Filename prefix
            timestamp: Timestamp for filename
            
        Returns:
            str: Generated filename
        """
        # Format timestamp for filename (replace colons for Windows compatibility)
        timestamp_str = timestamp.isoformat().replace(":", "-")
        return f"{prefix}_{timestamp_str}.json"
    
    def store_message(self, message_data: Dict[str, Any]) -> bool:
        """Store a contact message to file.
        
        Args:
            message_data: Message data dictionary
            
        Returns:
            bool: True if storage successful, False otherwise
        """
        try:
            filename = self._generate_filename("message", message_data["timestamp"])
            filepath = self.base_dir / "messages" / filename
            
            # Prepare data for JSON storage
            storage_data = {
                "type": "contact_message",
                "name": message_data["name"],
                "email": message_data["email"],
                "subject": message_data["subject"],
                "message": message_data["message"],
                "context": message_data["context"],
                "timestamp": message_data["timestamp"].isoformat(),
                "stored_at": datetime.now().isoformat()
            }
            
            # Write to file with proper encoding
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Stored message from {message_data['name']} to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store message: {e}")
            return False
    
    def store_confession(self, confession_data: Dict[str, Any]) -> bool:
        """Store a confession to file.
        
        Args:
            confession_data: Confession data dictionary
            
        Returns:
            bool: True if storage successful, False otherwise
        """
        try:
            filename = self._generate_filename("confession", confession_data["timestamp"])
            filepath = self.base_dir / "confessions" / filename
            
            # Prepare data for JSON storage
            storage_data = {
                "type": "confession",
                "confession": confession_data["confession"],
                "anonymous": confession_data.get("anonymous", True),
                "timestamp": confession_data["timestamp"].isoformat(),
                "stored_at": datetime.now().isoformat()
            }
            
            # Add identity info for open confessions
            if not confession_data.get("anonymous", True):
                storage_data["name"] = confession_data.get("name", "")
                storage_data["email"] = confession_data.get("email", "")
            
            # Write to file with proper encoding
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(storage_data, f, indent=2, ensure_ascii=False)
            
            confession_type = "anonymous" if storage_data["anonymous"] else "open"
            logger.info(f"Stored {confession_type} confession to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to store confession: {e}")
            return False
    
    def get_messages(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve stored messages.
        
        Args:
            limit: Maximum number of messages to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of message data
        """
        messages = []
        messages_dir = self.base_dir / "messages"
        
        if not messages_dir.exists():
            return messages
        
        try:
            # Get all message files, sorted by modification time (newest first)
            message_files = sorted(
                messages_dir.glob("message_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            for filepath in message_files[:limit]:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        message_data = json.load(f)
                    messages.append(message_data)
                except Exception as e:
                    logger.warning(f"Failed to load message file {filepath}: {e}")
            
        except Exception as e:
            logger.error(f"Failed to retrieve messages: {e}")
        
        return messages
    
    def get_confessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve stored confessions.
        
        Args:
            limit: Maximum number of confessions to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of confession data
        """
        confessions = []
        confessions_dir = self.base_dir / "confessions"
        
        if not confessions_dir.exists():
            return confessions
        
        try:
            # Get all confession files, sorted by modification time (newest first)
            confession_files = sorted(
                confessions_dir.glob("confession_*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            for filepath in confession_files[:limit]:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        confession_data = json.load(f)
                    confessions.append(confession_data)
                except Exception as e:
                    logger.warning(f"Failed to load confession file {filepath}: {e}")
            
        except Exception as e:
            logger.error(f"Failed to retrieve confessions: {e}")
        
        return confessions