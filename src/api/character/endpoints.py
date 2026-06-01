from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.api.character.dependencies import CharacterAgentServiceDependency
from src.api.character.schemas import CharacterMessageRequest, CharacterStateResponse
from src.api.general_schemas import ErrorResponse


router = APIRouter(prefix="/character", tags=["character-agent"])


@router.post("/chat", response_model=CharacterStateResponse)
async def chat_with_character(
    data: CharacterMessageRequest,
    agent_service: CharacterAgentServiceDependency,
) -> CharacterStateResponse | JSONResponse:
    """
    Send a message to the AI character agent.

    Request:
    {
        "chat_id": "demo-chat",
        "message": "Hi Nova, I like robotics."
    }

    Response:
    {
        "response": "...",
        "emotion": "...",
        "action": "...",
        "memory_update": "...",
        "used_tool": "..."
    }
    """
    try:
        return await agent_service.respond(
            chat_id=data.chat_id,
            message=data.message,
        )
    except Exception as error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(message=f"Agent error: {error}").model_dump(),
        )
