# db_service/app/database.py
import os
import time

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
Base = declarative_base()

MAX_RETRIES = 10
for i in range(MAX_RETRIES):
    try:
        engine = create_engine(os.getenv("DATABASE_URL", ""))
        Base.metadata.create_all(bind=engine)
        print("✅ Connected to the database!")
        break
    except OperationalError as e:
        print(f"⏳ Waiting for database... ({i + 1}/{MAX_RETRIES})")
        time.sleep(3)
else:
    raise RuntimeError("❌ Could not connect to the database after several attempts.")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)
