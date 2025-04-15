# orders_service/app/routes.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from user_service.app.security import get_current_user
from app.schemas import OrderCreate, OrderOut
from crud import create_order, get_orders_by_user, get_all_orders
from user_service.app.models import User

router = APIRouter()

@router.post("/orders/", response_model=OrderOut)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Создать новый заказ (только авторизованный пользователь)"""
    return create_order(db, current_user.id, order)

@router.get("/orders/", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Получить заказы (юзер - только свои, админ - все)"""
    if current_user.role == "ADMIN":
        return get_all_orders(db)
    return get_orders_by_user(db, current_user.id)
