# admin_service/app/routes.py
from fastapi import APIRouter, HTTPException
from app.grpc_clients.user import list_users, get_user_by_id
from app.grpc_clients.orders import get_all_orders, get_orders_by_user

router = APIRouter()

@router.get("/users/")
def get_users():
    return list_users()

@router.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        return get_user_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/orders/")
def get_orders():
    return get_all_orders()

@router.get("/orders/user/{user_id}")
def get_user_orders(user_id: int):
    return get_orders_by_user(user_id)
