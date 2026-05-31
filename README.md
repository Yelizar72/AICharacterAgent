# AI Character Agent MVP

A modular AI character agent built with FastAPI, Chainlit, LangChain, RAG, tool calling, and structured outputs.
The project uses OpenRouter with the DeepSeek V4 Pro model for LLM responses.

## Features

- FastAPI backend
- Chainlit frontend
- OpenRouter LLM integration
- DeepSeek V4 Pro model
- Personality-consistent AI character
- Short-term conversation memory
- RAG over a custom character profile
- Tool calling
- Structured output for response, emotion, action, and memory update
- Evaluation cases for memory consistency, personality stability, tool correctness, RAG grounding, and safety behavior

## Tech Stack

Python 3.11, uv, FastAPI, Chainlit, LangChain, Pydantic, OpenRouter, DeepSeek V4 Pro.

## Environment Variables

Create a local `.env` file:

```env
OPENROUTER_API_KEY=your_openrouter_key_here
OPENROUTER_MODEL=deepseek/deepseek-v4-pro
BACKEND_URL=http://127.0.0.1:8000

