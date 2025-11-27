from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

from src.router import router as api_router
from src.config import engine


def init_db():
    print("Creating tables (if not exist)...")
    SQLModel.metadata.create_all(engine)
    print("Tables ready")


app = FastAPI(
    title="Backend API of project Stock LLM NeuralProphet",
    description="Backend API of project Stock LLM NeuralProphet",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

init_db()
app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI project!"}
