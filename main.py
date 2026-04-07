"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1 import auth

app = FastAPI(title="FastAPI Auth Tutorial", version="1.0.0")

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI Auth Tutorial",
        version="1.0.0",
        description="Authentication and Authorization with FastAPI",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "description": "Enter your JWT token (without 'Bearer ' prefix)",
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete"]:
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get("/")
def root():
    return {"message": "FastAPI Auth Tutorial API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
