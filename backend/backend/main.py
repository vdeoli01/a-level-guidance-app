from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from backend.database import SessionLocal, User
# from sqlalchemy.orm import Session

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can also specify particular origins instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
import sys


# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}
#
# @app.get("/user")
# def get_user(db: Session = Depends(get_db)):
#     # Example to fetch the first user
#     user = db.query(User).first()
#     if user:
#         return {"username": user.username}
#     return {"message": "No users found!"}