from typing import List

from sqlalchemy.orm import Session

from src.database.models import Note, Tag
from src.schemas import NoteUpdate, NoteStatusUpdate, NoteModel

async def read_notes(skip: int, limit: int, db: Session) -> List[Note]:
    return db.query(Note).offset(skip).limit(limit).all()

async def create_note(body: NoteModel, db: Session) -> Note:
    tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
    
    note = Note(
        title=body.title,
        description=body.description,
        tags=tags
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

async def read_note(note_id: int, db: Session) -> Note | None:
    return db.query(Note).filter(Note.id==note_id).first()

async def update_note(note_id: int, body: NoteUpdate, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id==note_id).first()
    if note:
        tags = db.query(Tag).filter(Tag.id.in_(body.tags)).all()
        note.title = body.title
        note.description = body.description
        note.tags = tags
        note.done = body.done
        db.commit()
        db.refresh(note)
    return note

async def update_note_status(note_id: int, body: NoteStatusUpdate, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id==note_id).first()
    if note:
        note.done = body.done
        db.commit()
        db.refresh(note)
    return note

async def delete_note(note_id: int, db: Session) -> Note | None:
    note = db.query(Note).filter(Note.id==note_id).first()
    if note:
        db.delete(note)
        db.commit()
    return note