"""
Loads the trained TF-IDF + LogisticRegression models from model.joblib
and exposes simple predict functions for complaint category and priority.

Run train_model.py first to generate model.joblib.
"""

import joblib

from preprocessing import clean_text

_model_bundle = None


def _load():
    global _model_bundle
    if _model_bundle is None:
        try:
            _model_bundle = joblib.load("model.joblib")
        except FileNotFoundError as e:
            raise RuntimeError(
                "model.joblib not found. Run 'python train_model.py' first to train the models."
            ) from e
    return _model_bundle


def predict_category(text: str) -> dict:
    """Returns e.g. {"category": "Billing", "confidence": 0.87}"""
    bundle = _load()
    cleaned = clean_text(text)
    features = bundle["vectorizer"].transform([cleaned])

    prediction = bundle["category_model"].predict(features)[0]
    probabilities = bundle["category_model"].predict_proba(features)[0]
    confidence = max(probabilities)

    return {"category": prediction, "confidence": round(float(confidence), 4)}


def predict_priority(text: str) -> dict:
    """Returns e.g. {"priority": "high", "confidence": 0.72}"""
    bundle = _load()
    cleaned = clean_text(text)
    features = bundle["vectorizer"].transform([cleaned])

    prediction = bundle["priority_model"].predict(features)[0]
    probabilities = bundle["priority_model"].predict_proba(features)[0]
    confidence = max(probabilities)

    return {"priority": prediction, "confidence": round(float(confidence), 4)}
