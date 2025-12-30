from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from typing import List, Optional
import random

from models.database import get_db
from models.models import User, Vocabulary, UserVocabularyProgress, ReviewSession
from routers.auth import get_current_user

router = APIRouter(prefix="/api/vocab", tags=["vocabulary"])

# Pydantic models
class VocabularyResponse(BaseModel):
    id: int
    german: str
    spanish: str
    word_class: Optional[str]
    
    class Config:
        from_attributes = True

class QuizOption(BaseModel):
    vocab_id: int
    spanish: str

class QuizQuestion(BaseModel):
    vocab_id: int
    german: str
    options: List[QuizOption]
    word_class: Optional[str]

class ReviewSubmission(BaseModel):
    selected_vocab_id: int
    response_time_ms: Optional[int] = None

class ReviewResult(BaseModel):
    correct: bool
    correct_vocab_id: int
    correct_answer: str

class UserStats(BaseModel):
    total_reviews: int
    correct_reviews: int
    wrong_reviews: int
    accuracy: float
    words_learned: int
    words_due: int

# SM-2 Algorithm Implementation
def calculate_sm2_interval(
    quality: int,  # 0-5 (0-2 = wrong, 3-5 = correct)
    repetitions: int,
    ease_factor: float,
    interval_days: int
) -> tuple[int, float, int]:
    """
    Calculate next interval using SM-2 algorithm.
    Returns: (new_interval, new_ease_factor, new_repetitions)
    """
    if quality < 3:
        # Wrong answer: reset repetitions and interval
        repetitions = 0
        interval_days = 1
    else:
        # Correct answer
        ease_factor = max(1.3, ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        
        repetitions += 1
    
    return interval_days, ease_factor, repetitions

# Routes
@router.get("/next-review", response_model=QuizQuestion)
async def get_next_review(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get next vocabulary word for review with 4 multiple choice options."""
    
    # Get words that are due for review or haven't been seen yet
    current_time = datetime.utcnow()
    
    # First, check for due reviews
    due_progress_query = (
        select(UserVocabularyProgress)
        .where(
            and_(
                UserVocabularyProgress.user_id == current_user.id,
                UserVocabularyProgress.next_review <= current_time
            )
        )
        .order_by(UserVocabularyProgress.next_review)
        .limit(1)
    )
    result = await db.execute(due_progress_query)
    progress = result.scalar_one_or_none()
    
    if progress:
        # Load the vocabulary
        vocab_result = await db.execute(
            select(Vocabulary).where(Vocabulary.id == progress.vocab_id)
        )
        target_vocab = vocab_result.scalar_one()
    else:
        # No due reviews, get a new word that hasn't been seen
        seen_vocab_ids_query = select(UserVocabularyProgress.vocab_id).where(
            UserVocabularyProgress.user_id == current_user.id
        )
        seen_result = await db.execute(seen_vocab_ids_query)
        seen_ids = [row[0] for row in seen_result.all()]
        
        # Get unseen vocabulary
        unseen_query = select(Vocabulary).where(
            Vocabulary.id.notin_(seen_ids) if seen_ids else True
        ).order_by(Vocabulary.frequency_rank).limit(1)
        
        unseen_result = await db.execute(unseen_query)
        target_vocab = unseen_result.scalar_one_or_none()
        
        if not target_vocab:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No vocabulary available for review"
            )
        
        # Create new progress entry
        progress = UserVocabularyProgress(
            user_id=current_user.id,
            vocab_id=target_vocab.id
        )
        db.add(progress)
        await db.commit()
    
    # Generate 3 wrong answers from same word class
    wrong_answers_query = (
        select(Vocabulary)
        .where(
            and_(
                Vocabulary.id != target_vocab.id,
                Vocabulary.word_class == target_vocab.word_class
            )
        )
        .order_by(func.random())
        .limit(3)
    )
    wrong_result = await db.execute(wrong_answers_query)
    wrong_vocabs = wrong_result.scalars().all()
    
    # If not enough same word class, get random words
    if len(wrong_vocabs) < 3:
        additional_query = (
            select(Vocabulary)
            .where(Vocabulary.id != target_vocab.id)
            .order_by(func.random())
            .limit(3 - len(wrong_vocabs))
        )
        additional_result = await db.execute(additional_query)
        wrong_vocabs.extend(additional_result.scalars().all())
    
    # Create options and shuffle
    options = [QuizOption(vocab_id=target_vocab.id, spanish=target_vocab.spanish)]
    options.extend([
        QuizOption(vocab_id=v.id, spanish=v.spanish)
        for v in wrong_vocabs
    ])
    random.shuffle(options)
    
    return QuizQuestion(
        vocab_id=target_vocab.id,
        german=target_vocab.german,
        options=options,
        word_class=target_vocab.word_class
    )

@router.post("/{vocab_id}/review", response_model=ReviewResult)
async def submit_review(
    vocab_id: int,
    submission: ReviewSubmission,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit a review answer and update user progress using SM-2 algorithm."""
    
    # Check if answer is correct
    correct = submission.selected_vocab_id == vocab_id
    
    # Get or create progress
    progress_result = await db.execute(
        select(UserVocabularyProgress).where(
            and_(
                UserVocabularyProgress.user_id == current_user.id,
                UserVocabularyProgress.vocab_id == vocab_id
            )
        )
    )
    progress = progress_result.scalar_one_or_none()
    
    if not progress:
        progress = UserVocabularyProgress(
            user_id=current_user.id,
            vocab_id=vocab_id
        )
        db.add(progress)
    
    # Update statistics
    progress.times_seen += 1
    if correct:
        progress.times_correct += 1
    else:
        progress.times_wrong += 1
    
    # Calculate SM-2 values
    quality = 4 if correct else 0  # 4 = correct, 0 = wrong
    interval_days, ease_factor, repetitions = calculate_sm2_interval(
        quality,
        progress.repetitions,
        progress.ease_factor,
        progress.interval_days
    )
    
    progress.interval_days = interval_days
    progress.ease_factor = ease_factor
    progress.repetitions = repetitions
    progress.last_reviewed = datetime.utcnow()
    progress.next_review = datetime.utcnow() + timedelta(days=interval_days)
    
    # If wrong, schedule sooner (between 3-20 questions)
    if not correct:
        # Estimate ~20 seconds per question, schedule between 1-7 minutes
        minutes_delay = random.randint(1, 7)
        progress.next_review = datetime.utcnow() + timedelta(minutes=minutes_delay)
    
    # Record review session
    review_session = ReviewSession(
        user_id=current_user.id,
        vocab_id=vocab_id,
        was_correct=correct,
        response_time_ms=submission.response_time_ms
    )
    db.add(review_session)
    
    await db.commit()
    
    # Get correct answer
    vocab_result = await db.execute(
        select(Vocabulary).where(Vocabulary.id == vocab_id)
    )
    vocab = vocab_result.scalar_one()
    
    return ReviewResult(
        correct=correct,
        correct_vocab_id=vocab_id,
        correct_answer=vocab.spanish
    )

@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user vocabulary learning statistics."""
    
    # Get all user progress
    progress_result = await db.execute(
        select(UserVocabularyProgress).where(
            UserVocabularyProgress.user_id == current_user.id
        )
    )
    all_progress = progress_result.scalars().all()
    
    total_reviews = sum(p.times_seen for p in all_progress)
    correct_reviews = sum(p.times_correct for p in all_progress)
    wrong_reviews = sum(p.times_wrong for p in all_progress)
    
    accuracy = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0.0
    
    words_learned = len([p for p in all_progress if p.times_correct >= 3])
    
    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
    words_due = len([p for p in all_progress if p.next_review <= current_time])
    
    return UserStats(
        total_reviews=total_reviews,
        correct_reviews=correct_reviews,
        wrong_reviews=wrong_reviews,
        accuracy=round(accuracy, 2),
        words_learned=words_learned,
        words_due=words_due
    )

@router.get("/list", response_model=List[VocabularyResponse])
async def list_vocabulary(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """List all vocabulary words."""
    query = (
        select(Vocabulary)
        .order_by(Vocabulary.frequency_rank)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    return result.scalars().all()
