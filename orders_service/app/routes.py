from fastapi import APIRouter, Security
from app.dependencies import get_current_user
from app.grpc_client import (
    create_order_grpc,
    get_orders_for_user,
    get_all_orders_grpc,
)
from app.schemas import OrderCreate, OrderOut

router = APIRouter()

@router.post("/orders/", response_model=OrderOut)
def create_new_order(
    order: OrderCreate,
    current_user = Security(get_current_user)
):
    grpc_order = create_order_grpc(order, current_user.id)
    return OrderOut.from_grpc(grpc_order)

@router.get("/orders/", response_model=list[OrderOut])
def get_orders(current_user = Security(get_current_user)):
    if current_user.role == "ADMIN":
        grpc_orders = get_all_orders_grpc()
    else:
        grpc_orders = get_orders_for_user(current_user.id)

    return [OrderOut.from_grpc(order) for order in grpc_orders]
