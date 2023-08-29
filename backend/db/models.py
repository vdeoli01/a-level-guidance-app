from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'
    uid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    name: Mapped[str]
    password_hash: Mapped[str]
    salt: Mapped[str]

    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship()
    slots: Mapped[List["Slot"]] = relationship()


class Quiz(Base):
    __tablename__ = 'quiz'
    uid: Mapped[int] = mapped_column(primary_key=True)

    questions: Mapped[List["Question"]] = relationship()
    quiz_attempts: Mapped[List["QuizAttempt"]] = relationship()


class Question(Base):
    __tablename__ = 'question'
    uid: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey('quiz.uid'))
    question: Mapped[str]

    question_responses: Mapped[List["QuestionResponse"]] = relationship()


class Response(Base):
    __tablename__ = 'response'
    uid: Mapped[int] = mapped_column(primary_key=True)
    answer: Mapped[str]

    question_responses: Mapped[List["QuestionResponse"]] = relationship()


class QuizAttempt(Base):
    __tablename__ = 'quiz_attempt'
    uid: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.uid'))
    quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.uid'))
    end_time: Mapped[datetime]
    subjects: Mapped[str]

    question_responses: Mapped[List["QuestionResponse"]] = relationship()


class Slot(Base):
    __tablename__ = 'slot'
    uid: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('user.uid'))
    start_time: Mapped[datetime]
    advisor_name: Mapped[str]


class QuestionResponse(Base):
    __tablename__ = 'question_response'
    quiz_attempt_id: Mapped[int] = mapped_column(ForeignKey('quiz_attempt.uid'), primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('question.uid'), primary_key=True)
    response_id: Mapped[int] = mapped_column(ForeignKey('response.uid'), primary_key=True)
