from fastapi import FastAPI

app = FastAPI(title="AI Character Agent MVP")


@app.get("/")
async def root():
    return {
        "message": "Backend is running",
        "provider": "OpenRouter",
        "model": "deepseek/deepseek-v4-pro"
    }
