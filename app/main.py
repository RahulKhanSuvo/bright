from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.database import Base, engine

# Automatically create database tables if they don't exist
# Note: In production, you should use Alembic migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bright Blog API",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js
        "http://localhost:5173",  # Vite
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register API routers
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "API is running"}
