"""
Nexus AI Engine — Sidecar for AI operations.
LangGraph multi-agent orchestrator + RAG pipeline + LiteLLM routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Nexus AI Engine", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-engine"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
