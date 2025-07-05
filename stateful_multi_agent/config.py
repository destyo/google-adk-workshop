"""Configuration settings for the customer service multiagent system."""

import os
from typing import Dict, Any


class DatabaseConfig:
    """Database configuration settings."""
    
    # Default SQLite database path
    DEFAULT_DB_PATH = "./customer_service_data.db"
    
    # Database URL format
    DB_URL_TEMPLATE = "sqlite:///{db_path}"
    
    @classmethod
    def get_db_url(cls, db_path: str = None) -> str:
        """Get the database URL.
        
        Args:
            db_path: Custom database path (optional)
            
        Returns:
            Database URL string
        """
        if db_path is None:
            db_path = os.getenv("CUSTOMER_SERVICE_DB_PATH", cls.DEFAULT_DB_PATH)
        
        return cls.DB_URL_TEMPLATE.format(db_path=db_path)


class AppConfig:
    """Application configuration settings."""
    
    # Default app settings
    DEFAULT_APP_NAME = "Customer Support"
    DEFAULT_USER_ID = "aiwithantony"
    
    # Session management
    MAX_SESSIONS_PER_USER = 10
    CLEANUP_OLD_SESSIONS = True
    
    # Initial state template
    INITIAL_STATE_TEMPLATE = {
        "user_name": "Antony Dos Santos",
        "purchased_courses": [],
        "interaction_history": [],
    }
    
    @classmethod
    def get_app_name(cls) -> str:
        """Get the application name."""
        return os.getenv("CUSTOMER_SERVICE_APP_NAME", cls.DEFAULT_APP_NAME)
    
    @classmethod
    def get_user_id(cls) -> str:
        """Get the default user ID."""
        return os.getenv("CUSTOMER_SERVICE_USER_ID", cls.DEFAULT_USER_ID)
    
    @classmethod
    def get_initial_state(cls, user_name: str = None) -> Dict[str, Any]:
        """Get the initial state for a new session.
        
        Args:
            user_name: Custom user name (optional)
            
        Returns:
            Initial state dictionary
        """
        state = cls.INITIAL_STATE_TEMPLATE.copy()
        if user_name:
            state["user_name"] = user_name
        return state


class AgentConfig:
    """Agent configuration settings."""
    
    # Model settings
    DEFAULT_MODEL = "gemini-2.0-flash"
    
    # Agent behavior
    ENABLE_CONVERSATION_HISTORY = True
    ENABLE_STATE_PERSISTENCE = True
    
    @classmethod
    def get_model(cls) -> str:
        """Get the default model name."""
        return os.getenv("CUSTOMER_SERVICE_MODEL", cls.DEFAULT_MODEL)


# Example environment variables that can be set:
# CUSTOMER_SERVICE_DB_PATH=./custom_db.db
# CUSTOMER_SERVICE_APP_NAME=My Customer Service
# CUSTOMER_SERVICE_USER_ID=custom_user
# CUSTOMER_SERVICE_MODEL=gemini-1.5-pro
