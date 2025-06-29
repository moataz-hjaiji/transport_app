from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import true

from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.admin import AdminCreate
from app.models.admin import Admin
from app.schemas.admin import AdminOut,AdminUpdate

from app.auth.auth_handler import get_password_hash
from app.auth.dependencies import get_current_admin
from app.auth.auth_handler import oauth2_scheme, decode_token
from app.schemas.token import TokenData
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix="/api/admins",
    tags=["admins"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
def get_admins(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
    ):
    admins = db.query(Admin).offset(skip).limit(limit).all()
    return admins

@router.post("/")
def create_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    db_user = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(admin.password)
    db_user = Admin(
        email=admin.email,
        username=admin.username,
        password=hashed_password,
        is_active=admin.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Admin created successfully","data":db_user}


@router.get("/{admin_id}", response_model=AdminOut)
def get_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    
    return db_admin
@router.put("/{admin_id}",response_model=AdminOut)
def update_admin(admin_id: int,data: AdminUpdate,db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_admin, field, value)
    
    # 4. Commit changes
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    
    return db_admin
@router.delete("/{admin_id}")
def delete_admin(admin_id: int,db: Session = Depends(get_db)):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    # if db_admin.id == current_admin.id:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Cannot delete your own account"
    #     )
    db.delete(db_admin)
    db.commit()
    return None

@router.put("/{admin_id}/activate",response_model=AdminOut)
def active_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    admin.is_active = True
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
@router.put("/{admin_id}/desactive",response_model=AdminOut)
def active_admin(admin_id: int, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Admin with id {admin_id} not found"
        )
    admin.is_active = False
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin