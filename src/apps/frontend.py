import os
from uuid import uuid4

import chainlit as cl
import httpx
from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
CHARACTER_CHAT_ENDPOINT = f"{BACKEND_URL}/api/v1/character/chat"


def format_agent_response(data: dict) -> str:
    """
    Convert structured backend JSON into a readable Chainlit message.
    """
    response = data.get("response", "No response returned.")
    emotion = data.get("emotion", "unknown")
    action = data.get("action", "unknown")
    memory_update = data.get("memory_update")
    used_tool = data.get("used_tool")

    content = response

    content += "\n\n---"
    content += f"\n**Emotion:** `{emotion}`"
    content += f"\n**Action:** `{action}`"

    if used_tool:
        content += f"\n**Used tool:** `{used_tool}`"

    if memory_update:
        content += f"\n**Memory update:** `{memory_update}`"

    return content


@cl.on_chat_start
async def on_chat_start():
    """
    Runs when a new Chainlit chat session starts.
    We create a chat_id and store it in Chainlit user_session.
    """
    chat_id = str(uuid4())
    cl.user_session.set("chat_id", chat_id)

    welcome_message = (
        "Hi, I’m **Nova** 👋\n\n"
        "I’m an AI character agent with:\n"
        "- short-term memory\n"
        "- RAG over my character profile\n"
        "- tool calling\n"
        "- structured emotion/action outputs\n\n"
        "Try these messages:\n"
        "- `Hi Nova, I like robotics and PCB design.`\n"
        "- `What do I like?`\n"
        "- `Tell me your backstory.`\n"
        "- `calculate: 24 / 3 + 5`"
    )

    await cl.Message(content=welcome_message).send()


@cl.on_message
async def on_message(message: cl.Message):
    """
    Runs every time the user sends a message.
    Sends the message to FastAPI backend and displays Nova's response.
    """
    chat_id = cl.user_session.get("chat_id")

    if not chat_id:
        chat_id = str(uuid4())
        cl.user_session.set("chat_id", chat_id)

    payload = {
        "chat_id": chat_id,
        "message": message.content,
    }

    thinking_message = cl.Message(content="Nova is thinking...")
    await thinking_message.send()

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                CHARACTER_CHAT_ENDPOINT,
                json=payload,
            )

        response.raise_for_status()
        data = response.json()

        thinking_message.content = format_agent_response(data)
        await thinking_message.update()

    except httpx.ConnectError:
        thinking_message.content = (
            "I could not connect to the FastAPI backend.\n\n"
            "Please make sure it is running:\n\n"
            "`uv run fastapi dev src/apps/backend.py --port 8000`"
        )
        await thinking_message.update()

    except httpx.HTTPStatusError as error:
        thinking_message.content = (
            "The backend returned an error.\n\n"
            f"**Status code:** `{error.response.status_code}`\n\n"
            f"**Response:** `{error.response.text}`"
        )
        await thinking_message.update()

    except Exception as error:
        thinking_message.content = (
            "Unexpected frontend error.\n\n"
            f"`{type(error).__name__}: {error}`"
        )
        await thinking_message.update()
