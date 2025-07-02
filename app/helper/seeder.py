from app.helper.check_if_model_empty import check_if_empty_and_execute
from app.models.admin import Admin
from .seed.admin import seedAdmin
from app.database.database import SessionLocal


async def seeder():
    db = SessionLocal()
    try:
        await check_if_empty_and_execute(Admin, lambda: seedAdmin(db), db)
    finally:
        db.close()