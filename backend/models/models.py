from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from models.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    progress = relationship("UserVocabularyProgress", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("ReviewSession", back_populates="user", cascade="all, delete-orphan")


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True)
    german = Column(String(255), nullable=False)
    spanish = Column(String(255), nullable=False)
    word_class = Column(String(50), nullable=True)  # noun, verb, adjective, etc.
    difficulty = Column(Integer, default=1)  # 1-5 scale
    frequency_rank = Column(Integer, nullable=True, index=True)
    example_de = Column(Text, nullable=True)
    example_es = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    progress = relationship("UserVocabularyProgress", back_populates="vocabulary")
    reviews = relationship("ReviewSession", back_populates="vocabulary")


class UserVocabularyProgress(Base):
    __tablename__ = "user_vocabulary_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vocab_id = Column(Integer, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False)
    
    # Progress tracking
    times_seen = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    times_wrong = Column(Integer, default=0)
    
    # SM-2 algorithm fields
    ease_factor = Column(Float, default=2.5)  # SM-2 ease factor
    interval_days = Column(Integer, default=0)  # Current interval in days
    repetitions = Column(Integer, default=0)  # Number of successful repetitions
    
    # Scheduling
    last_reviewed = Column(DateTime(timezone=True), nullable=True)
    next_review = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="progress")
    vocabulary = relationship("Vocabulary", back_populates="progress")


class ReviewSession(Base):
    __tablename__ = "review_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vocab_id = Column(Integer, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False)
    was_correct = Column(Boolean, nullable=False)
    response_time_ms = Column(Integer, nullable=True)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="reviews")
    vocabulary = relationship("Vocabulary", back_populates="reviews")
