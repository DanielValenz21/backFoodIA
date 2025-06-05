from fastapi import FastAPI
from .auth import router as auth_router
from .predict import router as predict_router

app = FastAPI(title="Food API (FastAPI)")

app.include_router(auth_router)
app.include_router(predict_router)

@app.get("/")
def root():
    return {"msg": "Food API running"}
