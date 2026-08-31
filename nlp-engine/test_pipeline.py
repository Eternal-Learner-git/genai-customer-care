"""
Quick manual test - runs a few sample complaints through the full pipeline
and prints the results, so you can eyeball whether predictions look sane
before wiring this into the backend.

Run with: python test_pipeline.py
"""

from pipeline import analyze_complaint

test_complaints = [
    "I was charged twice for my order and nobody has refunded me yet, this is really frustrating.",
    "The app keeps crashing every time I open it, please fix this urgently.",
    "My package never arrived even though tracking says it was delivered three days ago.",
    "Just wanted to say thanks, the support agent resolved my issue really quickly today.",
    "Someone accessed my account without my permission, I need this locked down right now.",
]

if __name__ == "__main__":
    for complaint in test_complaints:
        print("=" * 70)
        print(f"Complaint: {complaint}")
        result = analyze_complaint(complaint)
        for key, value in result.items():
            print(f"  {key}: {value}")
    print("=" * 70)
