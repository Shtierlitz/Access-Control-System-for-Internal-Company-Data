# user_service/app/schemas.py

from pydantic import BaseModel, EmailStr


class LoginSchema(BaseModel):
    user_email: EmailStr
    password: str


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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
