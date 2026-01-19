from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from .database import Base


def generate_id():
    return str(uuid.uuid4())[:8]

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    notepad_id = Column(String, ForeignKey("notepads.id"), nullable=False)
    image_url = Column(String, nullable=True)
    ocr = Column(Text, nullable=True)
    memo = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    notepad = relationship("Notepad", back_populates="notes")

class Notepad(Base):
    __tablename__ = "notepads"

    id = Column(String, primary_key=True, default=generate_id)
    all_analysis = Column(Text, nullable=True)

    notes = relationship("Note", back_populates="notepad", cascade="all, delete-orphan")