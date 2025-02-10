from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from utils import verify_password
from database import get_db
from crud import create_user, get_users, get_user_by_id, get_user_by_email
from schemas import UserCreate, UserOut

router = APIRouter()

@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, str(user.email))
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, str(user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    return create_user(db, user)


@router.get("/users/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_users(db, skip, limit)


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return db_user
