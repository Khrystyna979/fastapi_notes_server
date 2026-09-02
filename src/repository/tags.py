from typing import List

from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas import TagModel

async def read_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()

async def create_tag(body: TagModel, db: Session) -> Tag:
    tag = Tag(name=body.name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

async def read_tag(tag_id: int, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id==tag_id).first()
    return tag

async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id==tag_id).first()
    if tag:
        tag.name = body.name
        db.commit()
        db.refresh(tag)
    return tag

async def delete_tag(tag_id: int, db: Session) -> Tag | None:
    tag = db.query(Tag).filter(Tag.id==tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
    return tag
    
