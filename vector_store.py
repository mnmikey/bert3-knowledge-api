import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

# 👇 Connect to Qdrant Cloud
client = QdrantClient(
    url=os.getenv("QDRANT_HOST"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "bert3_docs"

# 🔧 Ensure collection exists
def ensure_collection_exists():
    existing = client.get_collections().collections
    if not any(col.name == COLLECTION_NAME for col in existing):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
        )

ensure_collection_exists()

# ✅ Add vectors to Qdrant
def add_to_vector_store(vectors, metadata_list=None):
    points = []
    for i, vector in enumerate(vectors):
        payload = metadata_list[i] if metadata_list else {}
        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload=payload
        )
        points.append(point)

    client.upsert(collection_name=COLLECTION_NAME, points=points)

# 🔍 Semantic search
def semantic_search(query_vector, top_k=5):
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k
    )
    return results
