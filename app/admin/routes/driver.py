from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import true

from app.database.database import get_db
from sqlalchemy.orm import Session
from app.schemas.driver import DriverCreate,DriverOut,DriverUpdate
from app.models.driver import Driver
from app.auth.auth_handler import admin_only, get_password_hash
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix="/drivers",
    tags=["drivers"],
    dependencies=[admin_only]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
async def get_drivers(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    ):
    drivers = db.query(Driver).offset(skip).limit(limit).all()
    return drivers

@router.post("/")
def create_driver(driver: DriverCreate, db: Session = Depends(get_db)):
    db_user = db.query(Driver).filter(Driver.email == driver.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(driver.password)
    db_user = Driver(
        email=driver.email,
        first_name=driver.first_name,
        last_name=driver.last_name,
        password=hashed_password,
        is_active=driver.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "Driver created successfully","data":db_user}


@router.get("/{admin_id}", response_model=DriverOut)
def get_driver(
    admin_id: int,
    db: Session = Depends(get_db)
):
    db_driver = db.query(Driver).filter(Driver.id == admin_id).first()
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {admin_id} not found"
        )
    
    return db_driver
@router.put("/{admin_id}",response_model=DriverOut)
def update_driver(admin_id: int,data: DriverUpdate,db: Session = Depends(get_db)):
    db_driver = db.query(Driver).filter(Driver.id == admin_id).first()
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {admin_id} not found"
        )
    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_driver, field, value)
    
    # 4. Commit changes
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    
    return db_driver
@router.delete("/{admin_id}")
def delete_driver(admin_id: int,db: Session = Depends(get_db)):
    db_driver = db.query(Driver).filter(Driver.id == admin_id).first()
    if not db_driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {admin_id} not found"
        )
    db.delete(db_driver)
    db.commit()
    return None

@router.put("/{admin_id}/activate",response_model=DriverOut)
def active_driver(admin_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == admin_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {admin_id} not found"
        )
    driver.is_active = True
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver
@router.put("/{admin_id}/desactive",response_model=DriverOut)
def active_driver(admin_id: int, db: Session = Depends(get_db)):
    driver = db.query(Driver).filter(Driver.id == admin_id).first()
    if not driver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Driver with id {admin_id} not found"
        )
    driver.is_active = False
    db.add(driver)
    db.commit()
    db.refresh(driver)
    return driver