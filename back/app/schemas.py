from pydantic import BaseModel
from datetime import datetime


class NoteResponse(BaseModel):
    id: str
    notepad_id: str
    image_url: str | None = None
    ocr: str | None = None
    memo: str | None = None
    analysis: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    image_url: str | None = None
    ocr: str | None = None
    memo: str | None = None

class NoteUpdate(BaseModel):
    image_url: str | None = None
    ocr: str | None = None
    memo: str | None = None
    analysis: str | None = None

class NotepadResponse(BaseModel):
    id: str
    all_analysis: str | None = None
    notes: list[NoteResponse] = []

    class Config:
        from_attributes = True


# functions
class UploadResponse(BaseModel):
    image_url: str

class OcrRequest(BaseModel):
    image_url: str

class OcrResponse(BaseModel):
    ocr: str

class AnalyzeRequest(BaseModel):
    image_url: str | None = None
    ocr: str | None = None
    memo: str | None = None

class AnalyzeResponse(BaseModel):
    analysis: str