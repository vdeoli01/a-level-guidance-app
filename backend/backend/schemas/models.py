from datetime import datetime
from typing import List, Optional
from fastapi_users import schemas
from pydantic import BaseModel
import uuid

from db.models import UserRole



class UserRead(schemas.BaseUser[int]):
    name: str
    role: UserRole


class UserCreate(schemas.BaseUserCreate):
    name: str
    role: Optional[UserRole] = UserRole.NORMAL


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[UserRole]


class QuestionResponseBase(BaseModel):
    """Stores a users response to a question"""
    question_id: int
    response_id: int


class ResultsBase(BaseModel):
    """Stores a users results to a quiz"""
    subjects: List[str]


class SlotsBase(BaseModel):
    """Stores all possible slots and users associated"""
    start_time: datetime
    end_time: datetime
    advisor_name: str
    user_id: Optional[int] = None


class QuestionBase(BaseModel):
    """Stores a quiz question"""
    question_id: int
    question: str


class QuizBase(BaseModel):
    """Stores the quiz questions"""
    quiz_id: int


class QuizAttemptBase(BaseModel):
    """Stores the quiz attempt"""
    quiz_attempt_id: int
    user_id: int
    quiz_id: int
    end_time: datetime
    question_responses: List[QuestionResponseBase]
    subjects: List[str]
