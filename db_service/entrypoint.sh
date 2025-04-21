#!/bin/sh

cd /app

echo "⚙️ Running migrations..."
alembic upgrade head

echo "🚀 Starting gRPC server..."
python app/grpc_server.py &

echo "🚀 Starting gRPC OrderService..."
python app/grpc_order_server.py &


echo "🚀 Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
