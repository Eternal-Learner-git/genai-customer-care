"""
Builds the FAISS vector index from the knowledge base documents.

Pipeline: load .txt files -> split into overlapping chunks -> embed each chunk
with a HuggingFace sentence-transformer model -> store in a FAISS index on disk.

Run this once to build the index, and re-run it any time knowledge_base/ changes:
    python ingest.py
"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

KNOWLEDGE_BASE_DIR = "knowledge_base"
INDEX_DIR = "faiss_index"

# all-MiniLM-L6-v2 is small (~80MB), fast on CPU, and a common default for RAG embeddings.
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def build_index():
    print(f"Loading documents from {KNOWLEDGE_BASE_DIR}/ ...")
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="*.txt", loader_cls=TextLoader)
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s)")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    print(f"Loading embedding model ({EMBEDDING_MODEL})... this downloads once, ~80MB")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Embedding chunks and building FAISS index...")
    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local(INDEX_DIR)
    print(f"Saved FAISS index to {INDEX_DIR}/")


if __name__ == "__main__":
    build_index()
