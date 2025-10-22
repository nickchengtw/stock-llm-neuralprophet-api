from fastapi import FastAPI
from src.api.get_stocks import router as api_router

app = FastAPI(
    title="Backend API of project Stock LLM NeuralProphet",
    description="Backend API of project Stock LLM NeuralProphet",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to the FastAPI project!"}
