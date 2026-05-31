from typing import Literal, Optional

from pydantic import BaseModel, Field


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


class CharacterMessageRequest(BaseModel):
    chat_id: str = Field(
        examples=["demo-chat"],
        description="Unique chat/session ID used for memory.",
    )
    message: str = Field(
        examples=["Hi Nova, I like robotics and PCB design."],
        description="User message.",
    )


class CharacterStateResponse(BaseModel):
    response: str = Field(
        description="Natural language reply from the AI character.",
    )
    emotion: EmotionType = Field(
        description="Current emotional state of the character.",
    )
    action: ActionType = Field(
        description="Fake animation/action command for the character.",
    )
    memory_update: Optional[str] = Field(
        default=None,
        description="Short memory update if the user shared useful information.",
    )
    used_tool: Optional[str] = Field(
        default=None,
        description="Name of the tool used, if any.",
    )
