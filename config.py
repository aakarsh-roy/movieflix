from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))  # Load SECRET_KEY from .env or generate a default
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/movieflix")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"  # Convert to boolean
    SESSION_COOKIE_NAME = "movieflix_session"
    PERMANENT_SESSION_LIFETIME = 86400  # 1 day in seconds

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_URI = "mongodb://localhost:27017/test_movieflix"
