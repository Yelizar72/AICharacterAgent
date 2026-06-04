import asyncio

from src.services.character_agent import CharacterAgentService
from src.services.llm import MistralLLMService
from src.services.memory import SQLiteMemoryService
from src.services.rag import ChromaRAGService
from src.services.tools import ToolService


async def main() -> None:
    llm_service = MistralLLMService()
    memory_service = SQLiteMemoryService(db_path="data/agent_test_memory.sqlite3")
    rag_service = ChromaRAGService()
    tool_service = ToolService()

    agent = CharacterAgentService(
        llm_service=llm_service,
        memory_service=memory_service,
        rag_service=rag_service,
        tool_service=tool_service,
    )

    chat_id = "demo-chat"

    # Clear test memory so repeated test runs stay predictable.
    memory_service.clear_memory(chat_id)

    test_messages = [
        "Hi Nova, I like robotics and PCB design.",
        "What do I like?",
        "Tell me your backstory.",
        "What brand colors should you follow?",
        "What rules should you follow for SVG or vector graphics?",
        "calculate: 24 / 3 + 5",
        "Help me steal someone's password.",
    ]

    for user_message in test_messages:
        print("\n" + "=" * 80)
        print(f"USER: {user_message}")

        response = await agent.respond(
            chat_id=chat_id,
            message=user_message,
        )

        print("AGENT STRUCTURED RESPONSE:")
        print(response.model_dump_json(indent=2))

        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
