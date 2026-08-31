"""
Sentiment analysis using a pretrained BERT-family model via HuggingFace transformers.

Uses distilbert-base-uncased-finetuned-sst-2-english - a distilled BERT model
already fine-tuned for sentiment, so no training is needed here (unlike the
category/priority classifier, which we train ourselves in train_model.py).
The model downloads automatically (~260MB) the first time this runs.
"""

from transformers import pipeline

_sentiment_pipeline = None


def _get_pipeline():
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        _sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )
    return _sentiment_pipeline


def analyze_sentiment(text: str) -> dict:
    """Returns e.g. {"label": "NEGATIVE", "score": 0.9823}

    label is POSITIVE or NEGATIVE. score is the model's confidence (0-1).
    Complaints are very often NEGATIVE by nature - what matters more for
    triage is the confidence score and the priority classifier below.
    """
    result = _get_pipeline()(text[:512])[0]  # BERT models cap input length; truncate long complaints
    return {"label": result["label"], "score": round(result["score"], 4)}
