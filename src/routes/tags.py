from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import TagModel, TagResponse
from src.repository import tags as repository_tags

router = APIRouter(prefix='/tags', tags=["tags"])

@router.get('/', response_model=List[TagResponse])
async def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = await repository_tags.read_tags(skip, limit, db)
    return tags
    
@router.post('/', response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagModel, db: Session = Depends(get_db)):
    created_tag = await repository_tags.create_tag(tag, db)
    return created_tag
    
@router.get('/{tag_id}', response_model=TagResponse)
async def read_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = await repository_tags.read_tag(tag_id, db)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tag not found')
    return tag

@router.put('/{tag_id}', response_model=TagResponse)
async def update_tag(tag_id: int, tag: TagModel, db: Session = Depends(get_db)):
    updated_tag = await repository_tags.update_tag(tag_id, tag, db)
    if updated_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tag not found')
    return updated_tag
    
@router.delete('/{tag_id}', response_model=TagResponse)
async def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    deleted_tag = await repository_tags.delete_tag(tag_id, db)
    if deleted_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tag not found')
    return deleted_tag
