"""
Text preprocessing using spaCy.

Cleans raw complaint text before it goes into the classifier: lowercases,
removes stopwords/punctuation, and lemmatizes so the model sees consistent
word forms (e.g. "delivered", "delivering", "delivers" all become "deliver").
"""

import spacy

# en_core_web_sm is the small English pipeline - fast, no word vectors, fine for this task.
# Download it once with: python -m spacy download en_core_web_sm
_nlp = None


def _get_nlp():
    """Lazy-load the spaCy pipeline so importing this module doesn't require
    the model to be downloaded until it's actually used."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp


def clean_text(text: str) -> str:
    """Lowercase, remove stopwords/punctuation, and lemmatize the input text.

    Example:
        "I was charged twice for my order!!" -> "charge twice order"
    """
    nlp = _get_nlp()
    doc = nlp(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens)


def extract_entities(text: str) -> list[dict]:
    """Pull out named entities (dates, money amounts, org names, etc.) - useful
    later for showing admins quick context without reading the full complaint."""
    nlp = _get_nlp()
    doc = nlp(text)
    return [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
