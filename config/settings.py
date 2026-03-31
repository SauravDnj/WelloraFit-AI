"""
Application Settings and Configuration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application configuration"""
    
    # Application
    APP_NAME = "WelloraFit AI"
    VERSION = "1.0.0"
    
    # Groq API - Check both Streamlit secrets and environment variables
    @staticmethod
    def get_api_key():
        """Get API key from Streamlit secrets or environment"""
        try:
            import streamlit as st
            # Try Streamlit secrets first (for cloud deployment)
            if hasattr(st, 'secrets') and 'GROQ_API_KEY' in st.secrets:
                return st.secrets['GROQ_API_KEY']
        except:
            pass
        # Fall back to environment variable (for local development)
        return os.getenv("GROQ_API_KEY", "")
    
    GROQ_API_KEY = get_api_key.__func__()
    GROQ_TEXT_MODEL = "llama-3.3-70b-versatile"  # Updated to current model
    GROQ_VISION_MODEL = "llama-3.2-90b-vision-preview"
    
    # Database
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "journable.db")
    
    # File Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
    MAX_UPLOAD_SIZE_MB = 10
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    
    # Nutrition Defaults
    DEFAULT_DAILY_CALORIES = 2000
    DEFAULT_DAILY_PROTEIN = 150
    DEFAULT_DAILY_CARBS = 200
    DEFAULT_DAILY_FAT = 65
    DEFAULT_DAILY_WATER_ML = 2000
    
    # UI Settings
    PRIMARY_COLOR = "#00D9A3"  # Teal/green from reference UI
    SECONDARY_COLOR = "#1E1E1E"
    
    @staticmethod
    def validate():
        """Validate critical settings"""
        api_key = Settings.get_api_key()
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found. "
                "Streamlit Cloud: Add to app secrets. Local: Add to .env file."
            )
        
        # Create necessary directories
        os.makedirs(os.path.dirname(Settings.DATABASE_PATH), exist_ok=True)
        os.makedirs(Settings.UPLOAD_FOLDER, exist_ok=True)

# Create settings instance
settings = Settings()
