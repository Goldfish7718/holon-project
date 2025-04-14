from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Optional
from controllers import chat
from pydantic import BaseModel

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    language: Optional[str] = "en"

@router.post("/stream", response_class=StreamingResponse)
def stream_response(chat_request: ChatRequest):
    return chat.stream_response(chat_request.prompt, chat_request.language)   

@router.post("/generate")
def generate_response(chat_request: ChatRequest):
    return chat.generate_response(chat_request.prompt, chat_request.language)

@router.get("/history")
def get_history():
    return chat.get_chat_history()