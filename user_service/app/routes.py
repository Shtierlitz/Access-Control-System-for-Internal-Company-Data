from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from crud import create_user, get_users, get_user_by_id, get_user_by_email
from database import get_db
from models import User
from schemas import UserCreate, UserOut, LoginSchema
from security import create_access_token, verify_password, get_password_hash

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.user_email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": user.email, "role": user.role}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, str(user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

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
