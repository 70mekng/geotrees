from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from . import schemas, models
from .database import get_db
from .services.imgUpload import create_presigned_url

router = APIRouter()
DB = Annotated[Session, Depends(get_db)]

# Note
@router.post("/notepad/{notepad_id}/note", response_model=schemas.NoteResponse)
def create_note(notepad_id: str, data: schemas.NoteCreate, db: DB):
    notepad = db.query(models.Notepad).filter(models.Notepad.id == notepad_id).first()
    if not notepad:
        raise HTTPException(status_code=404, detail="Notepad not found")

    note = models.Note(
        notepad_id=notepad_id,
        image_url=data.image_url,
        ocr=data.ocr,
        memo=data.memo,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.patch("/note/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, data: schemas.NoteUpdate, db: DB):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.image_url = data.image_url
    note.ocr = data.ocr
    note.memo = data.memo
    note.analysis = data.analysis
    db.commit()
    db.refresh(note)
    return note


@router.delete("/note/{note_id}")
def delete_note(note_id: int, db: DB):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": f"Note {note_id} deleted successfully"}

# Notepad
@router.post("/notepad", response_model=schemas.NotepadResponse)
def create_notepad(db: DB):
    notepad = models.Notepad()
    db.add(notepad)
    db.commit()
    db.refresh(notepad)
    return notepad

@router.delete("/notepad")
def delete_empty_notepad(db: DB):
    subquery = db.query(models.Note.notepad_id).distinct()
    
    empty_notepads = (
        db.query(models.Notepad)
        .filter(~models.Notepad.id.in_(subquery))
        .all()
    )
    if not empty_notepads:
        return {"message": "No empty notepads found"}

    for notepad in empty_notepads:
        db.delete(notepad)
    
    db.commit()
    
    return {"message": f"Deleted {len(empty_notepads)} empty notepads."}


@router.get("/notepad/{notepad_id}", response_model=schemas.NotepadResponse)
def get_notepad(notepad_id: str, db: DB):
    notepad = db.query(models.Notepad).filter(models.Notepad.id == notepad_id).first()
    if not notepad:
        raise HTTPException(status_code=404, detail="Notepad not found")

    notepad.notes = db.query(models.Note).filter(models.Note.notepad_id == notepad_id).all()
    return notepad

@router.delete("/notepad/{notepad_id}")
def delete_notepad(notepad_id: str, db: DB):
    notepad = db.query(models.Notepad).filter(models.Notepad.id == notepad_id).first()
    if not notepad:
        raise HTTPException(status_code=404, detail="Notepad not found")
    db.delete(notepad)
    db.commit()
    return {"message": f"Notepad {notepad_id} deleted successfully"}


@router.post("/notepad/{notepad_id}/analyze", response_model=schemas.AnalyzeResponse)
def analyze_notepad(notepad_id: str, db: DB):
    # TODO
    pass

# Functions
@router.post("/upload", response_model=schemas.UploadResponse)
def upload_image(extension: str):
    upload_url, image_url = create_presigned_url(extension)
    return schemas.UploadResponse(upload_url=upload_url, image_url=image_url)


@router.post("/ocr", response_model=schemas.OcrResponse)
def ocr(data: schemas.OcrRequest):
    # TODO
    pass


@router.post("/analyze", response_model=schemas.AnalyzeResponse)
def analyze(data: schemas.AnalyzeRequest):
    # TODO
    pass