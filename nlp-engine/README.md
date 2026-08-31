# NLP Engine — GenAI Customer Care System

Complaint classification, sentiment analysis, and priority prediction.
This is the component that fills in the `category`, `sentiment`, and `priority`
fields on each complaint the backend stores.

## What's included

- **`preprocessing.py`** — spaCy-based text cleaning (lowercase, remove stopwords/punctuation, lemmatize)
- **`sentiment.py`** — sentiment analysis using a pretrained BERT model (DistilBERT fine-tuned for sentiment) — no training needed, works out of the box
- **`sample_data.csv`** — 48 labeled example complaints across 6 categories, used to train the classifiers
- **`train_model.py`** — trains a TF-IDF + Logistic Regression model for both category and priority, saves to `model.joblib`
- **`classifier.py`** — loads the trained model and predicts category/priority for new complaint text
- **`pipeline.py`** — combines everything into one function: `analyze_complaint(text)`
- **`test_pipeline.py`** — runs a few sample complaints through the pipeline so you can sanity-check the output

## ⚠️ Important: about the sample dataset

`sample_data.csv` has 48 examples — enough to prove the whole pipeline works end to end (text in → category, sentiment, priority out), but **too small for genuinely reliable predictions**. I tested this training setup and confirmed it correctly predicts things like "charged twice for my order" → `Billing / high`, but on held-out test data, accuracy is inconsistent because there just isn't enough data yet.

This is normal for a first working version, not a bug. Before this goes into your final capstone demo, you and your NLP teammate should:
1. Add many more labeled examples to `sample_data.csv` (aim for 200+ per category if possible — real or synthetic)
2. Re-run `train_model.py` after every meaningful addition to the dataset
3. Watch the classification report it prints — precision/recall per category should climb as you add data

## Setup

1. **Create a virtual environment** inside `nlp-engine/`:
   ```bash
   python -m venv venv
   ```
   Activate it (Windows PowerShell): `venv\Scripts\Activate.ps1`

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   Note: `torch` and `transformers` are large (~1-2GB combined) — this install will take a while and needs a decent internet connection.

3. **Download the spaCy language model** (separate from pip install):
   ```bash
   python -m spacy download en_core_web_sm
   ```

4. **Train the classifier:**
   ```bash
   python train_model.py
   ```
   This reads `sample_data.csv`, trains the category and priority models, prints accuracy reports, and saves everything to `model.joblib`. Re-run this any time you update the dataset.

5. **Test it:**
   ```bash
   python test_pipeline.py
   ```
   The first run will also download the BERT sentiment model (~260MB) automatically — that only happens once, it's cached after that.

   You should see output like:
   ```
   Complaint: I was charged twice for my order and nobody has refunded me yet...
     category: Billing
     category_confidence: 0.81
     sentiment: NEGATIVE
     sentiment_score: 0.9967
     priority: high
     priority_confidence: 0.68
   ```

## Folder structure

```
nlp-engine/
├── preprocessing.py     # spaCy text cleaning
├── sentiment.py          # BERT sentiment analysis
├── classifier.py          # loads model.joblib, predicts category/priority
├── train_model.py         # trains and saves the classifiers
├── pipeline.py             # analyze_complaint() - the main entry point
├── test_pipeline.py         # quick manual test
├── sample_data.csv           # training data (needs expanding, see warning above)
├── requirements.txt
└── model.joblib              # generated after you run train_model.py (not committed to git)
```

## Next integration point

Once this is tested and the dataset is expanded, the backend engineer needs to call
`analyze_complaint(text)` from `pipeline.py` right after a new complaint is created
in `POST /complaints`, then use the result to `PATCH /complaints/{id}` with the
category, sentiment, and priority. That wiring hasn't been done yet — this component
currently runs standalone.

`model.joblib` should be added to `.gitignore` in the project root — it's a generated
file, not source code, and can get large. Each teammate should run `train_model.py`
locally after cloning.
