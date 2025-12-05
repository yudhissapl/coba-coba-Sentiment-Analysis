from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from . import models, schemas
from modules.items.users.routes import get_current_user
from modules.items.users import models as user_models

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.post("/", response_model=schemas.FeedbackRead, status_code=status.HTTP_201_CREATED)
def create_feedback(
    fb_in: schemas.FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user),
):
    user_id = fb_in.user_id or current_user.id

    feedback = models.Feedback(
        statement=fb_in.statement,
        status=fb_in.status,
        sentiment=fb_in.sentiment,
        rating=fb_in.rating,
        product_id=fb_in.product_id,
        user_id=user_id,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/", response_model=List[schemas.FeedbackRead])
def list_feedback(
    db: Session = Depends(get_db),
    product_id: Optional[int] = None,
    sentiment: Optional[str] = None,
):
    query = db.query(models.Feedback)
    if product_id is not None:
        query = query.filter(models.Feedback.product_id == product_id)
    if sentiment is not None:
        query = query.filter(models.Feedback.sentiment == sentiment)
    return query.all()

@router.get("/sample", response_model=List[schemas.FeedbackRead])
def get_sample_feedback(db: Session = Depends(get_db)):
    """
    Mengembalikan 10 data feedback pertama dari DB.
    Ini bukan baca CSV, tapi data yang dipakai API.
    """
    rows = db.query(models.Feedback).limit(10).all()
    return rows

@router.get("/{feedback_id}", response_model=schemas.FeedbackRead)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback


@router.put("/{feedback_id}", response_model=schemas.FeedbackRead)
def update_feedback(
    feedback_id: int,
    fb_in: schemas.FeedbackUpdate,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user),
):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if current_user.role != "admin" and feedback.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted")

    if fb_in.statement is not None:
        feedback.statement = fb_in.statement
    if fb_in.status is not None:
        feedback.status = fb_in.status
    if fb_in.sentiment is not None:
        feedback.sentiment = fb_in.sentiment
    if fb_in.rating is not None:
        feedback.rating = fb_in.rating
    if fb_in.product_id is not None:
        feedback.product_id = fb_in.product_id
    if fb_in.user_id is not None:
        feedback.user_id = fb_in.user_id

    db.commit()
    db.refresh(feedback)
    return feedback


@router.delete("/{feedback_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_feedback(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user),
):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    if current_user.role != "admin" and feedback.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not permitted")

    db.delete(feedback)
    db.commit()
    return
