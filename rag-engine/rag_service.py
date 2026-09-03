"""
Exposes the RAG pipeline (rag_pipeline.py) as a small HTTP service, so the
main backend can call it without needing langchain/faiss/transformers/torch
installed in its own environment.

Run with: uvicorn rag_service:app --port 8002 --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

from rag_pipeline import generate_suggested_response

app = FastAPI(title="RAG Engine Service")


class GenerateRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate")
def generate(req: GenerateRequest):
    """Returns a suggested response and the source chunks used to ground it."""
    return generate_suggested_response(req.text)
