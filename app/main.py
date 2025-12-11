from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.chatbot_api import router as chatbot_router

app = FastAPI(title="WindyAI Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot_router, prefix="/api")

