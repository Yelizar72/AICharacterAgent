from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.character.endpoints import router as character_router


app = FastAPI(
    title="AI Character Agent MVP",
    description="FastAPI backend for a modular AI character agent with memory, RAG, tools, and structured output.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "AI Character Agent backend is running",
        "llm_provider": "Mistral AI",
        "model": "mistral-small-2506",
        "docs": "http://127.0.0.1:8000/docs",
    }


app.include_router(character_router, prefix="/api/v1")
