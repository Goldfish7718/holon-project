# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat, metrics

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}