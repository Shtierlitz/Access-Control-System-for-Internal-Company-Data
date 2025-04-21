from pydantic import BaseModel
from datetime import datetime


class OrderBase(BaseModel):
    item_name: str
    price: int


class OrderCreate(OrderBase):
    pass


class OrderOut(OrderBase):
    id: int
    created_at: datetime
    user_id: int
    status: str

    @classmethod
    def from_grpc(cls, grpc_order) -> "OrderOut":
        return cls(
            id=grpc_order.id,
            item_name=grpc_order.item_name,
            price=grpc_order.price,
            created_at=grpc_order.created_at,
            user_id=grpc_order.user_id,
            status=grpc_order.status,
        )

