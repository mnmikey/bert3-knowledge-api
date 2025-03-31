import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from uuid import uuid4

qdrant_url = os.getenv("QDRANT_URL")
qdrant_key = os.getenv("QDRANT_API_KEY")

client = QdrantClient(url=qdrant_url, api_key=qdrant_key)
COLLECTION_NAME = "bert3_docs"

# Create collection if it doesn't exist
try:
    client.get_collection(collection_name=COLLECTION_NAME)
except:
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

def upsert_vectors(chunks, embeddings):
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={"text": chunk}
        ) for chunk, embedding in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=COLLECTION_NAME, points=points)


def semantic_search(query):
    from services.embeddings import embed_chunks
    query_embedding = embed_chunks([query])[0]
    hits = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=5
    )
    return [hit.payload for hit in hits]
