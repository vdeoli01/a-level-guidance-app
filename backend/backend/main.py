from typing import List

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import User, Base
from sqlalchemy.orm import Session
from backend.schemas.user import UserBase

DATABASE_URL = "postgresql://test:test@postgres:5432/test-db"
# Initialize database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Initialise App
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify particular origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/user", response_model=List[UserBase])
def list_user(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Returns List of all users"""
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserBase(**user.__dict__) for user in users]
