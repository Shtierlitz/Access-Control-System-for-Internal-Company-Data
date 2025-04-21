from sqlalchemy.orm import Session
from db_service.app.models import Order
from db_service.app.schemas import OrderCreate


def create_order(db: Session, user_id: int, order_data: OrderCreate) -> Order:
    order = Order(
        user_id=user_id,
        item_name=order_data.item_name,
        price=order_data.price,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_orders_by_user(db: Session, user_id: int) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_all_orders(db: Session) -> list[Order]:
    return db.query(Order).all()
