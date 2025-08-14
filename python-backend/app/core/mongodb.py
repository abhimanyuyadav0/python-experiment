from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URL, MONGODB_DB_NAME
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Create database connection."""
    try:
        # Validate connection string
        if not MONGODB_URL or MONGODB_URL.strip() == "":
            raise ValueError("MONGODB_URL is empty or not configured")
        
        # Ensure proper MongoDB connection string format
        if not MONGODB_URL.startswith(('mongodb://', 'mongodb+srv://')):
            raise ValueError("MONGODB_URL must start with 'mongodb://' or 'mongodb+srv://'")
        
        # Create client with connection options
        mongodb.client = AsyncIOMotorClient(
            MONGODB_URL,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Test connection
        await mongodb.client.admin.command('ping')
        
        # Set database
        mongodb.db = mongodb.client[MONGODB_DB_NAME]
        
        print(f"✅ Connected to MongoDB: {MONGODB_DB_NAME}")
        logger.info(f"Connected to MongoDB database: {MONGODB_DB_NAME}")
        
    except Exception as e:
        error_msg = f"Failed to connect to MongoDB: {str(e)}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)
        raise

async def close_mongo_connection():
    """Close database connection."""
    try:
        if mongodb.client:
            mongodb.client.close()
            print("✅ MongoDB connection closed.")
            logger.info("MongoDB connection closed")
    except Exception as e:
        error_msg = f"Error closing MongoDB connection: {str(e)}"
        print(f"❌ {error_msg}")
        logger.error(error_msg)

def get_mongodb():
    """Get MongoDB database instance."""
    if mongodb.db is None:
        raise RuntimeError("MongoDB not connected. Call connect_to_mongo() first.")
    return mongodb.db
