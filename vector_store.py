import hashlib
import logging
import os
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from openai import OpenAI

COLLECTION_NAME = "bert3-docs"

client = QdrantClient(
    url=os.getenv("QDRANT_HOST", "http://localhost:6333")
)

# 🔒 Ensure collection exists
def ensure_collection_exists():
    existing = client.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in existing]:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=1536,
                distance=Distance.COSINE
            )
        )

ensure_collection_exists()

# ✅ Vector upload helper
def add_to_vector_store(embeddings, metadata):
    points = []
    for i, vector in enumerate(embeddings):
        point = PointStruct(
            id=hashlib.md5(f"{metadata['filename']}-{i}".encode()).hexdigest(),
            vector=vector,
            payload={
                "filename": metadata["filename"],
                "chunk_index": i,
                "text": metadata["chunks"][i]
            },
        )
        points.append(point)

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logging.info(f"✅ Added {len(points)} vectors for {metadata['filename']}")

# ✅ Semantic search helper
def semantic_search(query, top_k=5):
    openai = OpenAI()
    response = openai.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_vector = response.data[0].embedding

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
    )

    return [
        {
            "score": result.score,
            "text": result.payload.get("text"),
            "filename": result.payload.get("filename"),
            "chunk_index": result.payload.get("chunk_index")
        }
        for result in results
    ]
