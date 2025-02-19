from datetime import timedelta
import requests
from fastapi import APIRouter, Depends, HTTPException
from app.security import create_access_token, verify_password, get_password_hash, get_current_user, get_current_admin
from app.schemas import LoginSchema, UserCreate, UserOut, TokenResponse

DB_SERVICE_URL = "http://db_service:8000"

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema):
    response = requests.get(f"{DB_SERVICE_URL}/users/email/{data.user_email}")
    if response.status_code == 404:
        raise HTTPException(status_code=400, detail="User not found")

    user = response.json()

    if not verify_password(data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": user["email"], "role": user["role"]}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate):
    response = requests.get(f"{DB_SERVICE_URL}/users/email/{user.email}")
    if response.status_code == 200:
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_password = get_password_hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_password

    response = requests.post(f"{DB_SERVICE_URL}/users/", json=user_data)
    if response.status_code != 201:
        raise HTTPException(status_code=500, detail="Ошибка при создании пользователя")

    return response.json()


@router.get("/users/", response_model=list[UserOut])
def list_users(current_user=Depends(get_current_admin)):
    response = requests.get(f"{DB_SERVICE_URL}/users/")
    return response.json()


@router.get("/users/me", response_model=UserOut)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, current_user=Depends(get_current_admin)):
    response = requests.get(f"{DB_SERVICE_URL}/users/{user_id}")
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="User not found")
    return response.json()
