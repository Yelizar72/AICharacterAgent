import json
import os
import re
from abc import ABC, abstractmethod
from typing import Literal, Optional

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_mistralai import ChatMistralAI
from pydantic import BaseModel, Field, ValidationError


load_dotenv()


EmotionType = Literal[
    "happy",
    "curious",
    "thinking",
    "concerned",
    "neutral",
    "excited",
]

ActionType = Literal[
    "wave",
    "smile",
    "think",
    "explain",
    "encourage",
    "idle",
]


class CharacterStateDTO(BaseModel):
    response: str = Field(description="Natural language response from the character.")
    emotion: EmotionType = Field(description="Character emotion.")
    action: ActionType = Field(description="Character action or animation state.")
    memory_update: Optional[str] = Field(
        default=None,
        description="Short memory update if the user shared useful information.",
    )


class LLMService(ABC):
    @abstractmethod
    async def generate_character_state(
        self,
        system_prompt: str,
        user_message: str,
    ) -> CharacterStateDTO:
        raise NotImplementedError


class MistralLLMService(LLMService):
    def __init__(
        self,
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: Optional[int] = None,
    ) -> None:
        self.model_name = model_name or os.getenv("MISTRAL_MODEL", "mistral-small-2506")
        self.api_key = api_key or os.getenv("MISTRAL_API_KEY")

        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY is missing. Add it to your .env file.")

        self.max_tokens = max_tokens or self._get_max_tokens_from_env()

        self._llm = ChatMistralAI(
            model=self.model_name,
            api_key=self.api_key,
            temperature=temperature,
            max_tokens=self.max_tokens,
            timeout=60,
            max_retries=2,
        )

    @staticmethod
    def _get_max_tokens_from_env() -> int:
        raw_value = os.getenv("MISTRAL_MAX_TOKENS", "500")

        try:
            max_tokens = int(raw_value)
        except ValueError:
            raise ValueError("MISTRAL_MAX_TOKENS must be an integer, for example 500.")

        if max_tokens <= 0:
            raise ValueError("MISTRAL_MAX_TOKENS must be greater than 0.")

        return max_tokens

    async def generate_character_state(
        self,
        system_prompt: str,
        user_message: str,
    ) -> CharacterStateDTO:
        json_instruction = """
You must return ONLY valid JSON.
Do not use markdown.
Do not wrap the answer in ```json.

The JSON must have exactly these fields:
{
  "response": "string",
  "emotion": "happy | curious | thinking | concerned | neutral | excited",
  "action": "wave | smile | think | explain | encourage | idle",
  "memory_update": "string or null"
}

Rules:
- response must be the character's natural reply.
- emotion must be one of the allowed emotion values.
- action must be one of the allowed action values.
- memory_update must be null unless the user shares a useful preference, goal, or fact worth remembering.
- Keep the response concise.
"""

        messages = [
            SystemMessage(content=system_prompt.strip() + "\n\n" + json_instruction.strip()),
            HumanMessage(content=user_message),
        ]

        raw_response = await self._llm.ainvoke(messages)
        content = str(raw_response.content).strip()

        return self._parse_character_state(content)

    def _parse_character_state(self, content: str) -> CharacterStateDTO:
        """
        Parse model output into CharacterStateDTO.

        Mistral usually follows JSON instructions well, but this parser is defensive:
        1. Try direct JSON parsing.
        2. Try extracting the first JSON object.
        3. Return safe fallback if parsing fails.
        """
        try:
            data = json.loads(content)
            return CharacterStateDTO.model_validate(data)
        except (json.JSONDecodeError, ValidationError):
            pass

        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                return CharacterStateDTO.model_validate(data)
            except (json.JSONDecodeError, ValidationError):
                pass

        return CharacterStateDTO(
            response=content if content else "Sorry, I could not generate a valid response.",
            emotion="neutral",
            action="idle",
            memory_update=None,
        )
