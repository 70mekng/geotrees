from pydantic import BaseModel
from datetime import datetime


class NoteResponse(BaseModel):
    id: int
    notepad_id: str
    image_url: str
    ocr: str
    memo: str
    analysis: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    image_url: str
    ocr: str
    memo: str

class NoteUpdate(BaseModel):
    image_url: str
    ocr: str
    memo: str
    analysis: str

class NotepadResponse(BaseModel):
    id: str
    all_analysis: str | None = None
    notes: list[NoteResponse] = []

    class Config:
        from_attributes = True

# functions
class UploadResponse(BaseModel):
    upload_url: str
    image_url: str

class OcrRequest(BaseModel):
    image_url: str

class OcrResponse(BaseModel):
    ocr: str

# Analyze
class noteAnalyzeResponse(BaseModel):
    analysis: str

class notepadAnalyzeResponse(BaseModel):
    analysis: str
