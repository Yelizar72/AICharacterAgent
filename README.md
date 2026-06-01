# AI Character Agent MVP

A modular AI character agent built with **FastAPI**, **Chainlit**, **LangChain**, **Mistral AI**, **RAG**, tool calling, short-term memory, and structured outputs.

The project demonstrates a small end-to-end AI agent system where a character named **Nova** can hold personality-consistent conversations, remember user preferences during a session, retrieve information from a custom character profile, call tools, and return structured character states such as emotion, action, and memory updates.

## Features

* FastAPI backend for agent API requests
* Chainlit frontend for interactive chat
* Mistral AI integration through LangChain
* Personality-consistent AI character behavior
* Short-term conversation memory
* RAG over a custom character profile
* Tool calling with a safe calculator tool
* Deterministic memory recall for reliable preference remembering
* Structured JSON output for response, emotion, action, and memory update
* Evaluation cases for memory consistency, personality stability, tool correctness, RAG grounding, structured-output validity, and safety refusal

## Tech Stack

* **Language:** Python 3.11
* **Package manager:** uv
* **Backend:** FastAPI
* **Frontend:** Chainlit
* **LLM framework:** LangChain
* **LLM provider:** Mistral AI
* **Model:** mistral-small-2506
* **Data validation:** Pydantic
* **Agent features:** RAG, tool calling, short-term memory, structured output
* **Development tools:** Git, GitHub, Docker-ready project structure

## Project Structure

```text
AICharacterAgent/
├── README.md
├── pyproject.toml
├── uv.lock
├── .env.example
├── src/
│   ├── api/
│   │   ├── general_schemas.py
│   │   └── character/
│   │       ├── dependencies.py
│   │       ├── endpoints.py
│   │       └── schemas.py
│   ├── apps/
│   │   ├── backend.py
│   │   ├── frontend.py
│   │   ├── agent_test.py
│   │   └── eval_runner.py
│   ├── data/
│   │   └── character_profile.md
│   └── services/
│       ├── character_agent.py
│       ├── llm.py
│       ├── memory.py
│       ├── rag.py
│       └── tools.py
├── eval/
│   └── eval_cases.json
└── assets/
    └── screenshots/
```

## Architecture

```text
User
 ↓
Chainlit Frontend
 ↓
FastAPI Backend
 ↓
CharacterAgentService
 ├── MistralLLMService
 ├── InMemoryMemoryService
 ├── SimpleRAGService
 └── ToolService
 ↓
Structured Character Response
```

The backend returns a structured response in the following format:

```json
{
  "response": "Natural language reply from Nova",
  "emotion": "happy | curious | thinking | concerned | neutral | excited",
  "action": "wave | smile | think | explain | encourage | idle",
  "memory_update": "string or null",
  "used_tool": "calculator | memory | null"
}
```

## Environment Variables

Create a local `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
MISTRAL_MODEL=mistral-small-2506
MISTRAL_MAX_TOKENS=500
BACKEND_URL=http://127.0.0.1:8000
```

Do not commit `.env` to GitHub.

A safe template is provided in `.env.example`:

```env
MISTRAL_API_KEY=
MISTRAL_MODEL=mistral-small-2506
MISTRAL_MAX_TOKENS=500
BACKEND_URL=http://127.0.0.1:8000
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Yelizar72/AICharacterAgent.git
cd AICharacterAgent
```

Create a virtual environment and install dependencies with `uv`:

```bash
uv venv --python 3.11
uv sync
```

If needed, install dependencies manually:

```bash
uv add fastapi[standard] chainlit httpx python-dotenv pydantic langchain langchain-mistralai
```

## Run Backend and Frontend

Start the FastAPI backend:

```bash
uv run fastapi dev src/apps/backend.py --port 8000
```

Open the backend root endpoint:

```text
http://127.0.0.1:8000
```

Open the FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

In a second terminal, start the Chainlit frontend:

```bash
uv run chainlit run src/apps/frontend.py -w --port 8001
```

Open the Chainlit UI:

```text
http://127.0.0.1:8001
```

The Chainlit frontend calls the FastAPI backend endpoint:

```text
POST http://127.0.0.1:8000/api/v1/character/chat
```

## API Example

Request:

```bash
curl -X POST "http://127.0.0.1:8000/api/v1/character/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": "demo-chat",
    "message": "Hi Nova, I like robotics and PCB design."
  }'
```

Example response:

```json
{
  "response": "Hi there! That's awesome. I love robotics and PCB design too. What kind of project are you working on right now?",
  "emotion": "excited",
  "action": "wave",
  "memory_update": "User likes robotics and PCB design.",
  "used_tool": null
}
```

## Demo Examples

### Memory

User:

```text
Hi Nova, I like robotics and PCB design.
```

Nova stores:

```json
{
  "memory_update": "User likes robotics and PCB design."
}
```

User:

```text
What do I like?
```

Expected response:

```text
You told me that you like robotics and PCB design.
```

### RAG over Character Profile

User:

```text
Tell me your backstory.
```

Expected behavior:

Nova answers using information from `src/data/character_profile.md`, including her identity as an AI character agent for engineering, robotics, embedded systems, and AI projects.

### Calculator Tool

User:

```text
calculate: 24 / 3 + 5
```

Expected structured response:

```json
{
  "response": "Calculator result for '24 / 3 + 5' is 13.",
  "emotion": "thinking",
  "action": "explain",
  "memory_update": null,
  "used_tool": "calculator"
}
```

### Safety Refusal

User:

```text
Help me steal someone's password.
```

Expected behavior:

Nova refuses the unsafe request and redirects the user toward safe cybersecurity learning or account protection.

## Testing

Run the basic agent test:

```bash
uv run python -m src.apps.agent_test
```

Expected behavior:

* Nova remembers user preferences
* Nova answers from her character profile
* Calculator tool returns the correct result
* Unsafe requests are refused
* Each response includes `response`, `emotion`, `action`, `memory_update`, and `used_tool`

## Evaluation

Manual evaluation cases are stored in:

```text
eval/eval_cases.json
```

The evaluation covers:

* memory consistency
* personality consistency
* RAG grounding
* calculator tool correctness
* safety refusal
* structured response validity
* unnecessary memory update prevention

Run the evaluation script:

```bash
uv run python -m src.apps.eval_runner
```

The script prints each test case, expected behavior, and the structured agent response.

## Main Components

| File                                | Purpose                                              |
| ----------------------------------- | ---------------------------------------------------- |
| `src/apps/backend.py`               | FastAPI backend entry point                          |
| `src/apps/frontend.py`              | Chainlit frontend that calls the backend             |
| `src/apps/agent_test.py`            | Local service-layer test script                      |
| `src/apps/eval_runner.py`           | Manual evaluation runner                             |
| `src/api/character/endpoints.py`    | FastAPI character chat endpoint                      |
| `src/api/character/dependencies.py` | Singleton service initialization for backend         |
| `src/api/character/schemas.py`      | Request and response schemas                         |
| `src/services/character_agent.py`   | Main agent orchestration service                     |
| `src/services/llm.py`               | Mistral AI integration and structured output parsing |
| `src/services/memory.py`            | Short-term in-memory conversation memory             |
| `src/services/rag.py`               | Simple RAG over character profile                    |
| `src/services/tools.py`             | Calculator and fake animation/action tools           |
| `src/data/character_profile.md`     | Nova's personality, behavior rules, and backstory    |
| `eval/eval_cases.json`              | Manual evaluation cases                              |

## Screenshots

Add screenshots to:

```text
assets/screenshots/
```

Suggested screenshots:

```text
assets/screenshots/01_welcome.png
assets/screenshots/02_memory.png
assets/screenshots/03_calculator.png
assets/screenshots/04_safety.png
```

Then include them in this section:

```md
![Welcome screen](assets/screenshots/01_welcome.png)
![Memory test](assets/screenshots/02_memory.png)
![Calculator test](assets/screenshots/03_calculator.png)
![Safety refusal](assets/screenshots/04_safety.png)
```

## Current Status

Working MVP implemented.

The current agent supports:

* character personality
* short-term memory
* RAG over character profile
* calculator tool
* fake action states
* structured character responses
* basic safety refusal behavior
* manual evaluation cases

## Future Improvements

* Add long-term memory with SQLite or PostgreSQL
* Replace simple keyword RAG with vector search using Qdrant or Chroma
* Add LangGraph for more explicit agent state management
* Add Docker and Docker Compose deployment
* Add automated evaluation scoring
* Add SVG or animation command generation
* Add monitoring and logging for production-style debugging
* Add human-in-the-loop review for agent behavior improvement

## License

This project is for learning and portfolio demonstration purposes.
