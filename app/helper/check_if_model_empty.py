from typing import Type, Callable
from sqlalchemy.orm import Session
from fastapi import Depends
from app.database.database import get_db, SessionLocal

async def check_if_empty_and_execute(
    model: Type,
    callback: Callable[[], None],
    db: Session,
):
    count = db.query(model).count()
    if count == 0:
        callback()
