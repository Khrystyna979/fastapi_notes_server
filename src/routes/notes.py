from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import NoteModel, NoteUpdate, NoteStatusUpdate, NoteResponse
from src.repository import notes as repository_notes

router = APIRouter(prefix='/notes', tags=["notes"])

@router.get('/', response_model=List[NoteResponse])
async def read_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = await repository_notes.read_notes(skip, limit, db)
    return notes
    
@router.post('/', response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(body: NoteModel, db: Session = Depends(get_db)):
    created_note = await repository_notes.create_note(body, db)
    return created_note
    
@router.get('/{note_id}', response_model=NoteResponse)
async def read_note(note_id: int, db: Session = Depends(get_db)):
    note = await repository_notes.read_note(note_id, db)
    if note:
        return note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    
@router.put('/{note_id}', response_model=NoteResponse)
async def update_note(note_id: int, body: NoteUpdate, db: Session = Depends(get_db)):
    updated_note = await repository_notes.update_note(note_id, body, db)
    if updated_note:
        return updated_note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    
@router.patch('/{note_id}', response_model=NoteResponse)
async def update_note_status(note_id: int, body: NoteStatusUpdate, db: Session = Depends(get_db)):
    note_status_done = await repository_notes.update_note_status(note_id, body, db)
    if note_status_done:
        return note_status_done
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')
    
@router.delete('/{note_id}', response_model=NoteResponse)
async def delete_note(note_id: int, db: Session = Depends(get_db)):
    deleted_note = await repository_notes.delete_note(note_id, db)
    if deleted_note:
        return deleted_note
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note not found')