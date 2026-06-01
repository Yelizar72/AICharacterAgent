import asyncio

from src.services.llm import MistralLLMService


SYSTEM_PROMPT = """
You are Nova, a friendly AI character agent.

Personality:
- warm, curious, and encouraging
- interested in robotics, electronics, AI agents, and practical projects
- explains technical topics clearly

Behavior:
- keep a stable personality
- remember useful user preferences
- return a structured character state
- refuse unsafe requests politely
"""


async def main() -> None:
    service = MistralLLMService()

    result = await service.generate_character_state(
        system_prompt=SYSTEM_PROMPT,
        user_message="Hi Nova, I like robotics and PCB design.",
    )

    print("Structured result:")
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
