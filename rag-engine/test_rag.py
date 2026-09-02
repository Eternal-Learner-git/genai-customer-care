"""
Quick manual test - runs a few sample complaints through the RAG pipeline
and prints the suggested response plus which knowledge base chunks it used.

Run with: python test_rag.py
Make sure you've run 'python ingest.py' first to build the FAISS index.
"""

from rag_pipeline import generate_suggested_response

test_complaints = [
    "I was charged twice for my last order, can I get a refund?",
    "My package shows as delivered but I never received it.",
    "Someone logged into my account from a location I don't recognize.",
]

if __name__ == "__main__":
    for complaint in test_complaints:
        print("=" * 70)
        print(f"Complaint: {complaint}")
        result = generate_suggested_response(complaint)
        print(f"\nSuggested response:\n{result['suggested_response']}")
        print(f"\nRetrieved {len(result['sources'])} source chunk(s) used to ground this response.")
    print("=" * 70)
