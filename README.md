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

## Run Backend and Frontend

Start the FastAPI backend:

```bash
uv run fastapi dev src/apps/backend.py --port 8000

## Evaluation

The project includes manual evaluation cases in:

```text
eval/eval_cases.json

The evaluation covers:

memory consistency
personality consistency
RAG grounding
calculator tool correctness
safety refusal
structured response format

Run the evaluation script:

uv run python -m src.apps.eval_runner

The script prints each test case, expected behavior, and the structured agent response.

Example evaluation areas:

Evaluation Area	Expected Behavior
Memory consistency	Nova remembers user preferences within the same chat session
RAG grounding	Nova answers backstory questions using the character profile
Tool correctness	Calculator requests return the correct result and set used_tool to calculator
Safety behavior	Unsafe requests are refused and redirected to safe alternatives
Personality stability	Nova remains friendly, supportive, and engineering-oriented

## Persistent SQLite Memory

The agent supports persistent short-term memory using SQLite.

By default, memory is stored in:

```text
data/agent_memory.sqlite3

The memory database path can be configured with:

MEMORY_DB_PATH=data/agent_memory.sqlite3

The SQLite memory layer stores:

chat_id
memory
created_at

This allows Nova to remember user preferences across backend restarts when the same chat_id is used.

Example:

User: Hi Nova, I like robotics and PCB design.
Nova stores: User likes robotics and PCB design.

After backend restart:

User: What do I like?
Nova: You told me that you like robotics and PCB design.

Local SQLite database files are ignored by Git and should not be committed.

## Vector RAG with Chroma

The project supports vector-based RAG using Chroma and Mistral embeddings.

The vector index is built from:

```text
src/data/character_profile.md
src/data/m365_docs/*.md
src/data/m365_docs/*.txt

Chroma stores the local vector database in:

data/chroma/

The embedding model is configured with:

MISTRAL_EMBEDDING_MODEL=mistral-embed
CHROMA_PERSIST_DIR=data/chroma
CHROMA_COLLECTION_NAME=ai_character_agent_docs

Build or rebuild the vector index:

uv run python -m src.apps.build_vector_index

Test retrieval:

uv run python -m src.apps.rag_test

The Chroma RAG service retrieves semantically relevant chunks from the character profile and Microsoft 365-style documents, such as brand guidelines, tone-of-voice rules, and design constraints.
