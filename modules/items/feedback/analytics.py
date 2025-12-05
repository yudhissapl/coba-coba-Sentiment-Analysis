from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from . import models

router = APIRouter(
    prefix="/feedback/analytics",
    tags=["Feedback Analytics"],
)


@router.get("/status-counts")
def get_status_counts(db: Session = Depends(get_db)) -> Dict[str, List[Dict[str, int]]]:
    """
    Hitung jumlah data per status label (sesuai mental health dataset).
    Contoh response:
    {
        "status_counts": [
            {"status": "Anxiety", "count": 120},
            {"status": "Depression", "count": 80},
            ...
        ]
    }
    """
    rows = (
        db.query(
            models.Feedback.status,
            func.count(models.Feedback.id).label("count"),
        )
        .group_by(models.Feedback.status)
        .all()
    )

    return {
        "status_counts": [
            {"status": status, "count": count}
            for status, count in rows
        ]
    }


@router.get("/sentiment-counts")
def get_sentiment_counts(db: Session = Depends(get_db)) -> Dict[str, List[Dict[str, int]]]:
    """
    Hitung jumlah data per sentiment (kalo sudah diisi oleh model sentimen:
    positive / negative / neutral, dsb).

    Contoh response:
    {
        "sentiment_counts": [
            {"sentiment": "positive", "count": 100},
            {"sentiment": "negative", "count": 60},
            {"sentiment": "neutral", "count": 40}
        ]
    }
    """
    rows = (
        db.query(
            models.Feedback.sentiment,
            func.count(models.Feedback.id).label("count"),
        )
        .group_by(models.Feedback.sentiment)
        .all()
    )

    return {
        "sentiment_counts": [
            {"sentiment": sentiment, "count": count}
            for sentiment, count in rows
            if sentiment is not None
        ]
    }


@router.get("/status-by-sentiment")
def get_status_by_sentiment(db: Session = Depends(get_db)) -> Dict[str, List[Dict[str, int]]]:
    """
    Analitik silang status vs sentiment.
    Contoh response:
    {
        "status_by_sentiment": [
            {"status": "Anxiety", "sentiment": "negative", "count": 50},
            {"status": "Anxiety", "sentiment": "neutral", "count": 10},
            ...
        ]
    }
    """
    rows = (
        db.query(
            models.Feedback.status,
            models.Feedback.sentiment,
            func.count(models.Feedback.id).label("count"),
        )
        .group_by(models.Feedback.status, models.Feedback.sentiment)
        .all()
    )

    return {
        "status_by_sentiment": [
            {
                "status": status,
                "sentiment": sentiment,
                "count": count,
            }
            for status, sentiment, count in rows
            if sentiment is not None
        ]
    }
