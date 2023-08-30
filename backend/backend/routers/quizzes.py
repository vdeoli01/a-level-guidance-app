from fastapi import HTTPException
from typing import List
from fastapi import APIRouter, Depends
from backend.dependencies import get_db
from backend.schemas.models import QuizBase, QuestionBase
from db.models import Quiz, Question
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/quizzes",
    tags=["Quizzes"],
    responses={404: {"description": "Not found"}},
)


@router.get("/",
            response_model=List[QuizBase],
            )
def list_quizzes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Returns List of all users"""
    quizzes = db.query(Quiz).offset(skip).limit(limit).all()
    return [QuizBase(quiz_id=quiz.uid) for quiz in quizzes]


@router.get("/{quiz_id}/questions", response_model=List[QuestionBase])
def get_quiz_questions(quiz_id: int, db: Session = Depends(get_db)):
    """Returns questions associated with a quiz"""

    # Check if quiz exists
    quiz = db.query(Quiz).filter(Quiz.uid == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions = db.query(Question).filter(Question.quiz_id == quiz_id).all()
    if questions is None:
        raise HTTPException(status_code=404, detail="No Questions found")

    return [QuestionBase(question_id=q.uid, question=q.question) for q in questions]
