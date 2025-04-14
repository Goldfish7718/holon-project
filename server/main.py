# main.py
from fastapi import FastAPI
from routes import chat, metrics

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}