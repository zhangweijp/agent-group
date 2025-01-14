import os
from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Database configuration
    DB_PATH: str = os.getenv("DB_PATH", "database.db")
    
    # API configuration
    API_TITLE: str = "Project Management API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for managing projects, tasks, and members"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()

def get_db_url():
    return f"sqlite+aiosqlite:///{settings.DB_PATH}"
