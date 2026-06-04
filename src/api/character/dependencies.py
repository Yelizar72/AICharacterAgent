from typing import Annotated

from fastapi import Depends

from src.services.character_agent import CharacterAgentService
from src.services.llm import MistralLLMService
from src.services.memory import SQLiteMemoryService
from src.services.rag import SimpleRAGService
from src.services.tools import ToolService


# Singleton service instances.
# They are created once when the backend starts.
# SQLite memory persists even after backend restart.
llm_service = MistralLLMService()
memory_service = SQLiteMemoryService()
rag_service = SimpleRAGService()
tool_service = ToolService()

character_agent_service = CharacterAgentService(
    llm_service=llm_service,
    memory_service=memory_service,
    rag_service=rag_service,
    tool_service=tool_service,
)


def get_character_agent_service() -> CharacterAgentService:
    return character_agent_service


CharacterAgentServiceDependency = Annotated[
    CharacterAgentService,
    Depends(get_character_agent_service),
]
