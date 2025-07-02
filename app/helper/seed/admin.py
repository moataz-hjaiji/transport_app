import os

from fastapi import Depends
from sqlalchemy.orm import Session
from app.auth.auth_handler import get_password_hash
from app.database.database import get_db
from app.models.admin import Admin


def seedAdmin(db: Session):
    email = os.getenv('ADMIN_EMAIL')
    password = os.getenv('ADMIN_PASSWORD')
    username = os.getenv('ADMIN_USERNAME')
    hashed_password = get_password_hash(password)
    db_user = Admin(
        email=email,
        username=username,
        password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)