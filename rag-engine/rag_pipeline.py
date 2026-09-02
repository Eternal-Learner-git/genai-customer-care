"""
The main entry point for the RAG engine: takes a customer complaint and
returns a suggested response, grounded in the knowledge base via retrieval.

This is the function the backend will eventually call to fill in the
`suggested_response` field on a Complaint record.
"""

from retriever import retrieve_context
from llm import generate_response

PROMPT_TEMPLATE = """Policy information: {context}

Customer complaint: {complaint}

Write a short, specific reply to the customer using the policy information above. Mention what the customer should do next.

Reply:"""


def generate_suggested_response(complaint_text: str) -> dict:
    """
    Runs the full RAG pipeline: retrieve relevant policy chunks, build a
    grounded prompt, and generate a suggested response.

    Returns:
        {
            "suggested_response": "...",
            "sources": ["chunk 1 text...", "chunk 2 text...", ...]
        }
    """
    context_chunks = retrieve_context(complaint_text, k=2)
    context_text = "\n\n".join(context_chunks)

    prompt = PROMPT_TEMPLATE.format(context=context_text, complaint=complaint_text)
    response = generate_response(prompt)

    return {
        "suggested_response": response,
        "sources": context_chunks,
    }
