# db_service/app/models.py

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "user_service"}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="USER")

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "orders_service"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_service.users.id"))
    item_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
