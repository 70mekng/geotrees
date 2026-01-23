from fastapi import Depends
import os
from typing import Annotated
from sqlalchemy.orm import Session
from openai import OpenAI

from .. import schemas, models
from ..database import get_db

OPENAI_SECRET_KEY = os.getenv("OPENAI_SECRET_KEY")
if not OPENAI_SECRET_KEY:
    raise ValueError("OPENAI_SECRET_KEY is not set")
client = OpenAI(api_key=OPENAI_SECRET_KEY)

# Note Analyze
def openAi_note_analyze(note_id: int, db: Session):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise ValueError("Note not found")

    content = []
    if note.image_url:
        content.append({"type": "text", "text": "This is the image of the note."})
        content.append({"type": "image_url", "image_url": {"url": note.image_url}})
    if note.ocr:
        content.append({"type": "text", "text": f"OCR text extracted from image:\n{note.ocr}"})
    if note.memo:
        content.append({"type": "text", "text": f"Player's guess/notes:\n{note.memo}"})
    content.append({"type": "text", "text": "Based on the image and clues above, analyze and identify the location."})
    

    print('content', content)
    

    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "system",
                "content": """You are a GeoGuesser note analyzer expert assistant. 
                            Analyze the image and text clues to determine the location at whatever precision the evidence supports - from hemisphere down to street level.

                            Focus on:
                            - Sun/shadows: Hemisphere indicator
                            - Text/language: Script type, store names, signs from OCR
                            - Traffic: Driving side, road markings, license plates
                            - Infrastructure: Pole styles, bollards, road surface
                            - Landscape: Vegetation, terrain, climate
                            - Architecture: Building style, materials, roof type
                            - People: Clothing, visible demographics
                            - Other: Flags, brands, currency symbols

                            Output format (use plain text, NO markdown formatting like ** or #):
                            Precision: [one of: hemisphere / region / country / city / street]
                            Location: [Your estimate - only as precise as evidence allows]
                            Confidence: [Low/Medium/High]

                            Analysis:
                            - [Clue]: [What it suggests and why]
                            ...

                            Don't guess more specific than the evidence allows."""
            },
            {
                "role": "user", 
                "content": content
            }
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content


# Notepad Analyze
def openAi_notepad_analyze(notepad_id: str, db: Session):
    notes = db.query(models.Note).filter(models.Note.notepad_id == notepad_id).all()
    if not notes:
        raise ValueError("Notes not found")

    content = []
    content.append({"type": "text", "text": "Analyze the notes below and identify the location."})
    for note in notes:
        # if note.image_url:
        #     content.append({"type": "text", "text": "This is the image of the note."})
        #     content.append({"type": "image_url", "image_url": {"url": note.image_url}})
        if note.ocr:
            content.append({"type": "text", "text": f"OCR text extracted from image:\n{note.ocr}"})
        if note.memo:
            content.append({"type": "text", "text": f"Player's guess/notes:\n{note.memo}"})
        content.append({"type": "text", "text": "Based on the image and clues above, analyze and identify the location."})  

    response = client.chat.completions.create(
        model="gpt-4o",
        messages = [
            {
                "role": "system",
                "content": """You are a GeoGuesser analyst synthesizing multiple analysis notes from the same location.
                            Your task:
                            - Identify consistent clues that strengthen the conclusion
                            - Note contradictory clues that weaken confidence
                            - Combine clues to narrow down the location (e.g., language + architecture + infrastructure)
                            - Determine the most precise location the combined evidence supports

                            If evidence points to multiple possible locations, list them and explain what additional details from the images would help distinguish between them (e.g., specific text on visible signs, pole crossarm shape, license plate format).

                            Output format (plain text, no markdown):

                            Precision: (hemisphere / region / country / city / street)
                            Location: (your estimate)
                            Confidence: (low / medium / high)

                            Key evidence:
                            - [Clue combination]: [What it indicates]
                            ...

                            Conflicts or uncertainties:
                            - [List any contradictions or ambiguities]

                            Next steps to narrow down:
                            - [What to look for in the existing images based on current conclusion]"""
            },
            {
                "role": "user", 
                "content": content
            }
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content