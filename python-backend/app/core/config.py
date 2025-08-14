from dotenv import load_dotenv
import os

load_dotenv()

APP_NAME = os.getenv("PROJECT_NAME")
APP_VERSION = os.getenv("PROJECT_VERSION")
PORT = int(os.getenv("PORT", 5001))

# Database Configuration
# Use SQLite for development if PostgreSQL is not available
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./multitenant_app.db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "multitenant_app")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "datalake_db")

# JWT Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
