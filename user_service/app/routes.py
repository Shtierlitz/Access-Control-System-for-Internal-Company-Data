from datetime import timedelta
from typing import cast

import grpc
from fastapi import APIRouter, Depends, HTTPException
from app.security import create_access_token, verify_password, get_password_hash, get_current_user, get_current_admin
from app.schemas import LoginSchema, UserCreate, UserOut, TokenResponse
from app.grpc_client import get_user_by_email, get_user_by_id, create_user, list_users
from grpc import RpcError, StatusCode
router = APIRouter()

@router.post("/login", response_model=TokenResponse)
def login(data: LoginSchema):
    try:
        user = get_user_by_email(data.user_email)
    except grpc.RpcError as e:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token({"sub": user.email, "role": user.role}, timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/users/", response_model=UserOut)
def register_user(user: UserCreate):
    try:
        _ = get_user_by_email(user.email)
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")
    except grpc.RpcError:
        pass  # not found — можно создавать

    hashed_password = get_password_hash(user.password)
    created = create_user(user.username, user.email, hashed_password, user.role)
    return created


@router.get("/users/", response_model=list[UserOut])
def list_users_route(current_user=Depends(get_current_admin)):
    return list_users().users


@router.get("/users/me", response_model=UserOut)
def get_my_profile(current_user=Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, current_user=Depends(get_current_admin)):
    try:
        return get_user_by_id(user_id)
    except RpcError as e:
        err = cast(grpc._channel._InactiveRpcError, e)
        if err.code() == StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail="User not found")
        raise HTTPException(status_code=500, detail="Internal gRPC error")
