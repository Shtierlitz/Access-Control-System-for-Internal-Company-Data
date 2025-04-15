FROM python:3.12-slim

WORKDIR /app

COPY ./db_service/app /app/app
COPY ./requirements.txt /app/requirements.txt

COPY ./db_service/alembic.ini /app/alembic.ini
COPY ./db_service/migrations /app/migrations
COPY ./db_service/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh
RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT ["/entrypoint.sh"]
