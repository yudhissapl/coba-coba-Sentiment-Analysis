from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class FeedbackBase(BaseModel):
    statement: str
    status: str  # label dari dataset mental health (Anxiety, Depression, dll.)
    sentiment: Optional[str] = None  # hasil analisis sentimen (pos/neg/neutral)
    rating: Optional[int] = None     # rating 1–5


class FeedbackCreate(FeedbackBase):
    product_id: Optional[int] = None
    user_id: Optional[int] = None


class FeedbackUpdate(BaseModel):
    statement: Optional[str] = None
    status: Optional[str] = None
    sentiment: Optional[str] = None
    rating: Optional[int] = None
    product_id: Optional[int] = None
    user_id: Optional[int] = None


class FeedbackRead(BaseModel):
    id: int
    statement: str
    status: str
    sentiment: Optional[str] = None
    rating: Optional[int] = None
    product_id: Optional[int] = None
    user_id: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True
