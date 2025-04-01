import os
import uuid
import hashlib
import logging
from typing import List

import openai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http.models import Distance, VectorParams, SearchParams

COLLECTION_NAME = "bert3_vector_store"
EMBEDDING_MODEL = "text-embedding-ada-002"
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vector_store")


def ensure_collection_exists():
    collections = client.get_collections().collections
    if any(c.name == COLLECTION_NAME for c in collections):
        logger.info(f"Collection '{COLLECTION_NAME}' already exists")
        return

    logger.info(f"Creating collection '{COLLECTION_NAME}'")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
    )


def compute_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def add_to_vector_store(chunks: List[str], metadata: dict):
    ensure_collection_exists()

    logger.info(f"🔹 Sending {len(chunks)} chunks for embedding using model '{EMBEDDING_MODEL}'")
    response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=chunks,
    )

    embeddings = [res["embedding"] for res in response["data"]]
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "doc_id": metadata["doc_id"],
                "source": metadata["source"],
                "hash": compute_hash(chunk),
            },
        )
        for chunk, embedding in zip(chunks, embeddings)
    ]

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logger.info("✅ Data added to Qdrant successfully")


def semantic_search(query: str, doc_id: str, top_k: int = 5) -> List[str]:
    embedding = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )["data"][0]["embedding"]

    search_filter = Filter(
        must=[
            FieldCondition(key="doc_id", match=MatchValue(value=doc_id))
        ]
    )

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=embedding,
        query_filter=search_filter,
        limit=top_k,
        search_params=SearchParams(hnsw_ef=128, exact=False),
    )

    return [hit.payload["text"] for hit in results]
