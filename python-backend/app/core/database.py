from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# Create SQLAlchemy engine
print(f"🔧 Connecting to database: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=True)  # Enable SQL logging for debugging

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Alternative function for non-dependency injection usage
def get_db_session():
    return SessionLocal()
