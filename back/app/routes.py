from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from .database import get_db
from . import schemas, models

router = APIRouter()
DB = Annotated[Session, Depends(get_db)]

# Note
@router.post("/notepad/{notepad_id}/note", response_model=schemas.NoteResponse)
def create_note(notepad_id: str, data: schemas.NoteCreate, db: DB):
    # TODO
    pass


@router.patch("/note/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: str, data: schemas.NoteUpdate, db: DB):
    # TODO
    pass


@router.delete("/note/{note_id}")
def delete_note(note_id: str, db: DB):
    # TODO
    pass

# Notepad
@router.post("/notepad", response_model=schemas.NotepadResponse)
def create_notepad(db: DB):
    # TODO
    pass


@router.get("/notepad/{notepad_id}", response_model=schemas.NotepadResponse)
def get_notepad(notepad_id: str, db: DB):
    # TODO
    pass


@router.post("/notepad/{notepad_id}/analyze", response_model=schemas.AnalyzeResponse)
def analyze_notepad(notepad_id: str, db: DB):
    # TODO
    pass

# Functions
@router.post("/upload", response_model=schemas.UploadResponse)
def upload_image():
    # TODO
    pass


@router.post("/ocr", response_model=schemas.OcrResponse)
def ocr(data: schemas.OcrRequest):
    # TODO
    pass


@router.post("/analyze", response_model=schemas.AnalyzeResponse)
def analyze(data: schemas.AnalyzeRequest):
    # TODO
    pass