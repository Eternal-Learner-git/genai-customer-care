"""
The main entry point for the NLP engine: takes raw complaint text and
returns everything the backend needs to fill in on the Complaint record
(category, sentiment, priority).

This is the function the backend will eventually call - either directly
(if run in the same process) or wrapped in a small API, once you're ready
to wire the two components together.
"""

from classifier import predict_category, predict_priority
from sentiment import analyze_sentiment


def analyze_complaint(text: str) -> dict:
    """
    Runs the full NLP pipeline on a single complaint.

    Returns:
        {
            "category": "Billing",
            "category_confidence": 0.87,
            "sentiment": "NEGATIVE",
            "sentiment_score": 0.98,
            "priority": "high",
            "priority_confidence": 0.72,
        }
    """
    category_result = predict_category(text)
    priority_result = predict_priority(text)
    sentiment_result = analyze_sentiment(text)

    return {
        "category": category_result["category"],
        "category_confidence": category_result["confidence"],
        "sentiment": sentiment_result["label"],
        "sentiment_score": sentiment_result["score"],
        "priority": priority_result["priority"],
        "priority_confidence": priority_result["confidence"],
    }
