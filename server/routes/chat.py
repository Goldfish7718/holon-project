from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Optional
from controllers import chat
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    prompt: str
    language: Optional[str] = "en"

@router.post("/", response_class=StreamingResponse)
def generate_response(chat_request: ChatRequest):
    return chat.generate_response(chat_request.prompt, chat_request.language)   