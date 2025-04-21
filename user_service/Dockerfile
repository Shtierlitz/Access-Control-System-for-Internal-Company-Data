FROM python:3.12-slim

WORKDIR /app
COPY ./user_service/app /app/app
COPY ../requirements.txt /app/requirements.txt

COPY ./shared/generated /app/shared/generated
COPY ./shared/generated/__init__.py /app/shared/generated/__init__.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]
