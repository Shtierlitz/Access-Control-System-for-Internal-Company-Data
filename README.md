# 🚀 Access Control System for Internal Company Data

## Overview

This project is a pet project built for educational purposes only, created to explore and better understand microservices architecture, including key components such as Envoy (API Gateway), Open Policy Agent (OPA) for authorization, and gRPC for internal communication between services.
It provides a scalable, secure foundation for managing internal company data access, including user authentication, order management, and administrative controls, secured with JWT and OPA.
---

## 🔧 Stack of Technologies

- 🐳 Docker и Docker Compose
- ⚡️ FastAPI
- 🛠️ gRPC
- 🗄 PostgreSQL
- 🛡️ Envoy (API Gateway)
- 🔒 Open Policy Agent (OPA)

---

## 🛠️ Prerequisites

- Docker
- Docker Compose



## 📦 Project Structure

```
.
├── admin_service
│   ├── app
│   │   └── grpc_clients
│   └── .env
├── db_service
│   ├── app
│   └── .env
├── envoy
│   ├── envoy.yaml
│   └── policies
│       └── policy.rego
├── orders_service
│   ├── app
│   └── .env
├── user_service
│   ├── app
│   └── .env
├── shared
│   ├── __init__.py
│   ├── proto
│   │   ├── __init__.py
│   │   ├── orders.proto
│   │   └── user.proto
│   └── generated
│       ├── __init__.py
│       ├── orders_pb2.py
│       ├── orders_pb2_grpc.py
│       ├── user_pb2.py
│       └── user_pb2_grpc.py
├── .env.postgres
└── docker-compose.yml

```

---
## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Shtierlitz/Access-Control-System-for-Internal-Company-Data.git
cd Access-Control-System-for-Internal-Company-Data
```

### 2. Configure Environment Variables

Ensure you create the following `.env` files:

#### `.env.postgres`
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=api_gateway_db
```

#### `db_service/.env`
```env
DATABASE_URL=postgresql://postgres:your_password@postgres_db:5432/api_gateway_db
```

#### `user_service/.env`
```env
DB_SERVICE_URL=http://db_service:8000
USER_SERVICE_JWT_SECRET=your_jwt_secret
```

#### `orders_service/.env`
```env
SECRET_KEY=your_jwt_secret
```

### 3. Start services

```bash
docker-compose up --build
```

## 🔗 Services and Endpoints

### 🔐 User Service (`http://localhost:8002`)

| Method | Endpoint        | Description                                  |
|--------|-----------------|----------------------------------------------|
| POST   | `/users/login`  | Authenticate user and returns a JWT token.   |
| POST   | `/users/`       | Register a new user.                         |
| GET    | `/users/`       | List all users (Admin only).                 |
| GET    | `/users/me`     | Get the current user's profile.              |
| GET    | `/users/{id}`   | Get a specific user by ID (Admin only).      |

### 📦 Orders Service (`http://localhost:8003`)

| Method | Endpoint        | Description                                |
|--------|-----------------|--------------------------------------------|
| GET    | `/orders/`      | Retrieve all orders.                       |
| GET    | `/orders/{id}`  | Retrieve a specific order by ID.           |

### ⚙️ Admin Service (`http://localhost:8004`)

| Method | Endpoint                | Description                                       |
|--------|-------------------------|---------------------------------------------------|
| GET    | `/admin/`               | Check admin service health status.                |
| GET    | `/admin/users/`         | Retrieve all users (via gRPC).                    |
| GET    | `/admin/users/{id}`     | Retrieve user details by ID (via gRPC).           |
| GET    | `/admin/orders/`        | Retrieve all orders (via gRPC).                   |
| GET    | `/admin/orders/user/{id}`| Retrieve orders for a specific user by ID.       |

### 🔑 API Gateway (Envoy - `http://localhost:8080`)

| Method | Endpoint        | Service Routed       | Description                                 |
|--------|-----------------|----------------------|---------------------------------------------|
| POST   | `/login`        | User Service         | Authenticate and obtain JWT token           |
| GET    | `/users/...`    | User Service         | Access user endpoints via gateway           |
| GET    | `/orders/...`   | Orders Service       | Access orders endpoints via gateway         |
| GET    | `/admin/...`    | Admin Service        | Access administrative endpoints via gateway |

## 🔐 Security and Authorization

- **JWT (JSON Web Tokens)** used for securing endpoints.
- **OPA (Open Policy Agent)** defines authorization policies.

## 📝 Usage Examples

**Register a new user**:
```bash
curl -X POST http://localhost:8080/users/ -H "Content-Type: application/json" \
-d '{
  "username": "john_doe",
  "email": "user@example.com",
  "password": "your_password",
  "role": "USER"
}'
```
**Login and obtain JWT token:**
```bash
curl -X POST http://localhost:8080/login -H "Content-Type: application/json" \
-d '{"user_email": "user@example.com", "password": "your_password"}'
```

**Accessing protected endpoint:**
```bash
curl -X GET http://localhost:8080/users/me \
-H "Authorization: Bearer <JWT_TOKEN>"
```

## 🐳 Docker Compose Structure

- **db_service** - Database schema provider via gRPC
- **user_service** - Handles user management and authentication
- **orders_service** - Manages orders
- **admin_service** - Provides admin-level aggregation of data
- **postgres_db** - PostgreSQL database
- **envoy** - API Gateway
- **opa** - Authorization policy engine

## 📜 License

MIT License

---

Now you're ready to securely manage your company's internal data access with this comprehensive microservices setup!

