import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Application configuration."""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./crypto_notifier.db')
    
    # Application
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Alembic
    ALEMBIC_CONFIG = 'alembic.ini' 