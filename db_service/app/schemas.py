# db_service/app/schemas.py

from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: str = "USER"


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    user_email: str
    password: str


class TokenData(BaseModel):
    email: str
    role: str


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

    class Config:
        from_attributes = True


# --- User Schema with Orders ---
class UserWithOrders(UserOut):
    orders: list[OrderOut] = []
