"""
Trains the complaint category and priority classifiers on sample_data.csv
and saves them to model.joblib.

This uses scikit-learn: TF-IDF to turn text into numeric features, then a
LogisticRegression classifier for each target (category, priority). Both
share the same TF-IDF vectorizer so we only fit it once.

Run this once to produce model.joblib:
    python train_model.py

Re-run it any time sample_data.csv is updated with more/better examples -
the more real labeled complaints your team collects, the better this gets.
"""

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from preprocessing import clean_text


def train():
    df = pd.read_csv("sample_data.csv")
    print(f"Loaded {len(df)} labeled examples")

    print("Cleaning text with spaCy (this may take a moment)...")
    df["clean_text"] = df["text"].apply(clean_text)

    vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df["clean_text"])

    # Category model
    X_train, X_test, y_train, y_test = train_test_split(
        X, df["category"], test_size=0.2, random_state=42, stratify=df["category"]
    )
    category_model = LogisticRegression(max_iter=1000)
    category_model.fit(X_train, y_train)
    print("\n--- Category classifier ---")
    print(classification_report(y_test, category_model.predict(X_test), zero_division=0))

    # Priority model (trained on the full dataset's text -> priority mapping)
    X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
        X, df["priority"], test_size=0.2, random_state=42, stratify=df["priority"]
    )
    priority_model = LogisticRegression(max_iter=1000)
    priority_model.fit(X_train_p, y_train_p)
    print("\n--- Priority classifier ---")
    print(classification_report(y_test_p, priority_model.predict(X_test_p), zero_division=0))

    joblib.dump(
        {
            "vectorizer": vectorizer,
            "category_model": category_model,
            "priority_model": priority_model,
        },
        "model.joblib",
    )
    print("\nSaved trained models to model.joblib")


if __name__ == "__main__":
    train()
