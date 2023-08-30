from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://test:test@postgres:5432/test-db"
# Initialize database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
