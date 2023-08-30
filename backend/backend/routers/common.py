from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.models import User


def check_user_exists(user_id: int, db: Session):
    """Checks if a user exists, if not raise an exception"""
    user = db.query(User).filter(User.uid == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
