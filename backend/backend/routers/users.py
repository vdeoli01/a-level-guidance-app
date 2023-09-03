import json
from datetime import datetime
from random import sample
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.dependencies import get_async_session
from backend.routers.common import check_user_exists
from backend.routers.meetings import SLOT_LENGTH
from backend.schemas.models import QuizAttemptBase, QuestionResponseBase, SlotsBase
from backend.schemas.models import UserRead
from db.models import QuizAttempt, Quiz, QuestionResponse, Slot
from db.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

SUBJECTS = [
    "Maths",
    "English",
    "Science",
    "History",
    "Geography",
    "Art",
    "Music",
    "PE",
    "RE",
    "PSHE",
    "Computing",
]


# @router.get("/",
#             response_model=List[UserRead],
#             )
# async def list_user(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
#     """Returns List of all users"""
#     result = await session.scalars(select(User).offset(skip).limit(limit))
#     users = result.all()
#     return [UserRead(**user.__dict__) for user in users]
#
#
# @router.get("/{user_id}", response_model=UserRead)
# async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
#     """Returns a single user"""
#     result = await session.scalars(select(User).filter(User.id == user_id))
#     user = result.first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return UserRead(**user.__dict__)


@router.get("/{user_id}/quiz_attempts/{quiz_attempt_id}",
            response_model=QuizAttemptBase,
            )
async def get_quiz_attempt(
        user_id: int = Path(...),
        quiz_attempt_id: int = Path(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Get a quiz attempt"""
    await check_user_exists(user_id, session)

    # Check if quiz attempt exists
    result = await session.scalars(select(QuizAttempt).options(joinedload(QuizAttempt.question_responses)).filter(QuizAttempt.uid == quiz_attempt_id))
    quiz_attempt = result.first()
    if quiz_attempt is None:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")

    # Check if user owns this quiz attempt
    if quiz_attempt.user_id != user_id:
        raise HTTPException(status_code=403, detail="User does not own this quiz attempt")

    return QuizAttemptBase(
        quiz_attempt_id=quiz_attempt.uid,
        user_id=quiz_attempt.user_id,
        quiz_id=quiz_attempt.quiz_id,
        end_time=quiz_attempt.end_time,
        question_responses=[QuestionResponseBase(**qr.__dict__) for qr in quiz_attempt.question_responses],
        subjects=json.loads(quiz_attempt.subjects),
    )


@router.get("/{user_id}/quiz_attempts",
            response_model=List[QuizAttemptBase],
            )
async def list_quiz_attempts(
        user_id: int = Path(...),
        quiz_id: Optional[int] = Query(default=None),
        session: AsyncSession = Depends(get_async_session)
):
    """List all quiz attempts. Filter by quiz_id if provided"""
    await check_user_exists(user_id, session)

    query = select(QuizAttempt)

    if user_id is not None:
        query = query.filter(QuizAttempt.user_id == user_id)
    if quiz_id is not None:
        query = query.filter(QuizAttempt.quiz_id == quiz_id)

    result = await session.scalars(query)
    quiz_attempts = result.all()

    return [
        QuizAttemptBase(
            quiz_attempt_id=quiz_attempt.uid,
            user_id=quiz_attempt.user_id,
            quiz_id=quiz_attempt.quiz_id,
            end_time=quiz_attempt.end_time,
            question_responses=[QuestionResponseBase(**qr.__dict__) for qr in quiz_attempt.question_responses],
            subjects=json.loads(quiz_attempt.subjects),
        )
        for quiz_attempt
        in quiz_attempts
    ]


@router.post("/{user_id}/quiz_attempts", response_model=QuizAttemptBase)
async def calculate_quiz_attempt_results(
        user_id: int = Path(...),
        quiz_id: int = Body(...),
        question_responses: List[QuestionResponseBase] = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Calculates the results of a quiz attempt"""
    await check_user_exists(user_id, session)

    # Check if quiz exists
    result = await session.scalars(select(Quiz).filter(Quiz.uid == quiz_id))
    quiz = result.first()

    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # TODO implement the algorithm to calculate the results
    subjects = sample(SUBJECTS, 6)

    # Insert Quiz Attempt and Question Responses into DB
    quiz_attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        end_time=datetime.now(),
        subjects=json.dumps(subjects),
    )
    session.add(quiz_attempt)

    quiz_attempt.question_responses.extend(
        [
            QuestionResponse(
                question_id=qr.question_id,
                response_id=qr.response_id
            )
            for qr in question_responses
        ]
    )

    await session.commit()

    # return calculated results
    return QuizAttemptBase(
        quiz_attempt_id=quiz_attempt.uid,
        user_id=quiz_attempt.user_id,
        quiz_id=quiz_attempt.quiz_id,
        end_time=quiz_attempt.end_time,
        question_responses=quiz_attempt.question_responses,
        subjects=json.loads(quiz_attempt.subjects),
    )


@router.get("/{user_id}/slots",
            response_model=List[SlotsBase],
            )
async def list_booked_slots(
        user_id: int = Path(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Return list of all a users booked slots"""
    query = select(Slot)
    query = query.filter(Slot.user_id == user_id)
    results = await session.scalars(query)
    slots = results.all()

    return [
        SlotsBase(
            start_time=slot.start_time,
            end_time=slot.start_time + SLOT_LENGTH,
            advisor_name=slot.advisor_name,
            user_id=slot.user_id,
        )
        for slot in slots
    ]


# Book a slot for a user
@router.post("/{user_id}/slots",
             response_model=SlotsBase,
             )
async def book_slot(
        user_id: int = Path(...),
        slot_id: int = Body(...),
        session: AsyncSession = Depends(get_async_session)
):
    """Book a slot for a user"""
    await check_user_exists(user_id, session)

    # Check if slot is available
    slot = (await session.scalars(select(Slot).filter(Slot.uid == slot_id))).first()
    if slot is None:
        raise HTTPException(status_code=404, detail="Slot not found")
    if slot.user_id is not None:
        raise HTTPException(status_code=409, detail="Slot already booked")

    # Book slot
    slot.user_id = user_id
    await session.commit()

    return SlotsBase(
        start_time=slot.start_time,
        end_time=slot.start_time + SLOT_LENGTH,
        advisor_name=slot.advisor_name,
        user_id=slot.user_id,
    )
