from fastapi import FastAPI

from app.database import Base, engine

# Automatically create database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bright Blog API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"message": "API is running"}
