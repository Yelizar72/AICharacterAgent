# AI Character Agent MVP

A modular AI character agent built with FastAPI, Chainlit, LangChain, RAG, tool calling, short-term memory, and structured outputs.

The project uses Mistral AI with the `mistral-small-2506` model for LLM responses.

## Features

- FastAPI backend
- Chainlit frontend
- Mistral AI integration
- Personality-consistent AI character
- Short-term conversation memory
- RAG over a custom character profile
- Tool calling
- Structured output for response, emotion, action, and memory update
- Evaluation cases for memory consistency, personality stability, tool correctness, RAG grounding, and safety behavior

## Tech Stack

Python 3.11, uv, FastAPI, Chainlit, LangChain, Pydantic, Mistral AI, mistral-small-2506.

## Environment Variables

Create a local `.env` file with the following variables:

MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-small-2506
MISTRAL_MAX_TOKENS=500
BACKEND_URL=http://127.0.0.1:8000

Do not commit `.env` to GitHub.

## Current Status

Working MVP service layer is implemented.

The current agent supports:

- character personality
- short-term memory
- RAG over character profile
- calculator tool
- fake action states
- structured character responses
- basic safety refusal behavior

## How to Test

Run:

uv run python -m src.apps.agent_test

Expected behavior:

- Nova remembers user preferences
- Nova answers from her character profile
- Calculator tool returns a result
- Unsafe requests are refused
- Each response includes response, emotion, action, memory_update, and used_tool
