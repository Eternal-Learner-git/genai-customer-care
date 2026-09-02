"""
Loads the FAISS index built by ingest.py and retrieves the most relevant
knowledge base chunks for a given query (e.g. a customer complaint).
"""

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_DIR = "faiss_index"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

_vectorstore = None


def _load_vectorstore():
    global _vectorstore
    if _vectorstore is None:
        try:
            embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
            # allow_dangerous_deserialization is safe here since we're loading an index
            # we built ourselves in ingest.py, not one from an untrusted source.
            _vectorstore = FAISS.load_local(
                INDEX_DIR, embeddings, allow_dangerous_deserialization=True
            )
        except Exception as e:
            raise RuntimeError(
                f"Could not load FAISS index from {INDEX_DIR}/. "
                "Run 'python ingest.py' first to build it."
            ) from e
    return _vectorstore


def retrieve_context(query: str, k: int = 3) -> list[str]:
    """Returns the top-k most relevant knowledge base chunks for the query,
    as a list of plain text strings."""
    vectorstore = _load_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
