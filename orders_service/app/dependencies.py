# orders_service/app/dependencies.py
import os

import jwt
from app.grpc_client import get_user_by_email
from dotenv import load_dotenv
from fastapi import Request, HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")

ALGORITHM = "HS256"


def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token payload")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = get_user_by_email(email)
    return user
