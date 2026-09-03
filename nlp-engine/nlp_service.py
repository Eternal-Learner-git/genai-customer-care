"""
Exposes the NLP pipeline (pipeline.py) as a small HTTP service, so the main
backend can call it without needing spaCy/scikit-learn/transformers installed
in its own environment.

Run with: uvicorn nlp_service:app --port 8001 --reload
"""

from fastapi import FastAPI
from pydantic import BaseModel

from pipeline import analyze_complaint

app = FastAPI(title="NLP Engine Service")


class AnalyzeRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    """Returns category, sentiment, and priority predictions for the given text."""
    return analyze_complaint(req.text)
