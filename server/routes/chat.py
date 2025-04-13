from fastapi import APIRouter
from typing import Optional
from controllers import chat
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    prompt: str
    language: Optional[str] = "en"

@router.post("/")
def generate_response(chat_request: ChatRequest):
    return {
        "response": chat.generate_response(chat_request.prompt, chat_request.language)
    }