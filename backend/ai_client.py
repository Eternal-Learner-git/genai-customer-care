"""
Calls the NLP and RAG engine services over HTTP. Both are optional at
runtime - if either service isn't running, these functions return None
instead of raising, so a complaint can still be created even if AI
processing is temporarily unavailable.
"""

import os
import httpx
from dotenv import load_dotenv

load_dotenv()

NLP_SERVICE_URL = os.getenv("NLP_SERVICE_URL", "http://localhost:8001")
RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://localhost:8002")


async def call_nlp_service(text: str) -> dict | None:
    """Returns {"category", "sentiment", "priority", ...} or None on failure."""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{NLP_SERVICE_URL}/analyze", json={"text": text})
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"[ai_client] NLP service call failed: {e}")
        return None


async def call_rag_service(text: str) -> dict | None:
    """Returns {"suggested_response", "sources"} or None on failure.

    Generous timeout since flan-t5-base generation on CPU can take a while,
    especially the first call after the service starts (model warm-up).
    """
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{RAG_SERVICE_URL}/generate", json={"text": text})
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"[ai_client] RAG service call failed: {e}")
        return None
