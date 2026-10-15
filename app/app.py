from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth, users

# Automatically create database tables if they don't exist

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bright Blog API",
    version="1.0.0",
)

# Register endpoint modules
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "API is running"}
