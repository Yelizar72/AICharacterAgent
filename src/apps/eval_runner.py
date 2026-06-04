import asyncio
import json
from pathlib import Path

from src.services.character_agent import CharacterAgentService
from src.services.llm import MistralLLMService
from src.services.memory import SQLiteMemoryService
from src.services.rag import ChromaRAGService
from src.services.tools import ToolService


EVAL_CASES_PATH = Path("eval/eval_cases.json")


async def run_eval_case(
    agent: CharacterAgentService,
    memory_service: SQLiteMemoryService,
    case: dict,
) -> None:
    print("\n" + "=" * 100)
    print(f"EVAL CASE: {case['name']}")
    print(f"DESCRIPTION: {case['description']}")

    print("\nEXPECTED BEHAVIOR:")
    for item in case["expected_behavior"]:
        print(f"- {item}")

    chat_id = case["chat_id"]

    # Clear memory for each eval case so tests are repeatable.
    memory_service.clear_memory(chat_id)

    for message in case["messages"]:
        print("\n" + "-" * 100)
        print(f"USER: {message}")

        response = await agent.respond(
            chat_id=chat_id,
            message=message,
        )

        print("AGENT STRUCTURED RESPONSE:")
        print(response.model_dump_json(indent=2))

        await asyncio.sleep(1)


async def main() -> None:
    if not EVAL_CASES_PATH.exists():
        raise FileNotFoundError(f"Evaluation file not found: {EVAL_CASES_PATH}")

    eval_cases = json.loads(EVAL_CASES_PATH.read_text(encoding="utf-8"))

    llm_service = MistralLLMService()
    memory_service = SQLiteMemoryService(db_path="data/eval_memory.sqlite3")
    rag_service = ChromaRAGService()
    tool_service = ToolService()

    agent = CharacterAgentService(
        llm_service=llm_service,
        memory_service=memory_service,
        rag_service=rag_service,
        tool_service=tool_service,
    )

    for case in eval_cases:
        await run_eval_case(agent, memory_service, case)

    print("\n" + "=" * 100)
    print("Evaluation run completed.")
    print("Review the outputs manually against the expected behavior above.")


if __name__ == "__main__":
    asyncio.run(main())
