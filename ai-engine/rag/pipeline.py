"""
RAG Pipeline — Document chunking, embedding, and retrieval.
Uses pgvector for HNSW-indexed similarity search.
"""

from typing import List
import tiktoken


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]
        chunks.append(encoder.decode(chunk))
        start = end - overlap
    return chunks


def get_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    from openai import OpenAI
    client = OpenAI()
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


def search_similar(
    query: str,
    top_k: int = 5,
    threshold: float = 0.7,
) -> List[dict]:
    embedding = get_embedding(query)
    # TODO: Query pgvector with cosine similarity
    return []
