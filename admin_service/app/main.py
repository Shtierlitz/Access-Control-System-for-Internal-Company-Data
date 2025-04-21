# admin_service/app/main.py
from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Admin Service API")
app.include_router(router)