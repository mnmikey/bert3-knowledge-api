import hashlib
import logging
import os
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, SearchRequest
)
from qdrant_client.http.exceptions import ResponseHandlingException

import openai

logger = logging.getLogger("vector_store")
logging.basicConfig(level=logging.INFO)

# Env vars
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "bert3_vector_store")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Init Qdrant
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

def ensure_collection_exists():
    try:
        collections = client.get_collections().collections
        names = [c.name for c in collections]
        if QDRANT_COLLECTION_NAME not in names:
            logger.info(f"Creating collection '{QDRANT_COLLECTION_NAME}'")
            client.recreate_collection(
                collection_name=QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
            )
    except ResponseHandlingException as e:
        logger.error(f"Error ensuring collection exists: {e}")
        raise

ensure_collection_exists()

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def add_to_vector_store(embeddings_with_chunks, metadata={}, overwrite=False):
    points = []
    for item in embeddings_with_chunks:
        chunk_text = item["text"]
        embedding = item["embedding"]
        vector_id = compute_hash(chunk_text)

        point = PointStruct(
            id=vector_id,
            vector=embedding,
            payload={
                "text": chunk_text,
                **metadata,
            },
        )
        points.append(point)

    try:
        logger.info(f"Upserting {len(points)} vectors to Qdrant")
        client.upsert(collection_name=QDRANT_COLLECTION_NAME, points=points)
    except Exception as e:
        logger.error(f"Vector upsert failed: {e}")
        raise

def semantic_search(query: str, top_k: int = 5):
    try:
        logger.info("🔍 Performing semantic search")
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=query,
        )
        query_vector = response["data"][0]["embedding"]

        search_result = client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k
        )
        return [hit.payload for hit in search_result]
    except Exception as e:
        logger.error(f"❌ Semantic search failed: {e}")
        raise
