from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.dependencies import get_async_session
from backend.schemas.models import QuizBase, QuestionBase
from db.models import Quiz

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
            response_model=List[QuizBase],
            )
async def list_quizzes(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    """Returns List of all users"""
    quizzes = (await session.scalars(select(Quiz).offset(skip).limit(limit))).all()
    return [QuizBase(quiz_id=quiz.uid) for quiz in quizzes]


@router.get("/{quiz_id}/questions", response_model=List[QuestionBase])
async def get_quiz_questions(quiz_id: int, session: AsyncSession = Depends(get_async_session)):
    """Returns questions associated with a quiz"""

    # Check if quiz exists
    query = (
        select(Quiz)
        .filter(Quiz.uid == quiz_id)
    )
    quiz = (await session.scalars(query)).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    return [QuestionBase(question_id=q.uid, question=q.question) for q in quiz.questions]
