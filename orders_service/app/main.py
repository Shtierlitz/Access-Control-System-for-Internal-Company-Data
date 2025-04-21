# orders_service/app/main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.routes import router

app = FastAPI()
app.include_router(router)

# 👇 Swagger авторизация через Bearer Token
@app.get("/openapi.json", include_in_schema=False)
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Order Service API",
        version="1.0.0",
        description="Handles orders via gRPC",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi