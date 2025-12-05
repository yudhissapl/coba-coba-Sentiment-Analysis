from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)

    # kolom utama dari mental health dataset
    statement = Column(Text, nullable=False)      # isi teks kalimat
    status = Column(String(100), nullable=False)  # label asli (misal: Anxiety, Depression, dll.)

    # kolom tambahan dari project 2
    sentiment = Column(String(50), nullable=True)  # hasil analisis sentimen (pos/neg/neutral, dll.)
    rating = Column(Integer, nullable=True)        # rating 1–5 (opsional)

    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
