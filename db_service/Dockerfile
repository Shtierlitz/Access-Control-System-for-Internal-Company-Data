FROM python:3.12-slim

WORKDIR /app

COPY ./db_service/app /app/app
COPY ./requirements.txt /app/requirements.txt

COPY ./db_service/alembic.ini /app/alembic.ini
COPY ./db_service/migrations /app/migrations
COPY ./db_service/entrypoint.sh /entrypoint.sh
COPY ./shared /app/shared

RUN chmod +x /entrypoint.sh
RUN pip install --no-cache-dir -r /app/requirements.txt

RUN python -m grpc_tools.protoc \
    -I /app \
    --python_out=/app/shared/generated \
    --grpc_python_out=/app/shared/generated \
    shared/proto/user.proto \
    shared/proto/orders.proto \
 && touch /app/shared/generated/__init__.py





ENV PYTHONPATH=/app

ENTRYPOINT ["/entrypoint.sh"]
