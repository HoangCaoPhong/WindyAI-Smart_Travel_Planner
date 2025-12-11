from fastapi import APIRouter, Request
from core.algo6_chatbot.chatbot_engine import chatbot

router = APIRouter()

@router.post("/chat")
async def chat_handler(req: Request):
    body = await req.json()
    query = body.get("query", "")
    return chatbot(query)
