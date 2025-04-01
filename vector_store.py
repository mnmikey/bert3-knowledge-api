import os
import hashlib
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance, Filter, FieldCondition, MatchValue
from uuid import uuid4
from datetime import datetime

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

def compute_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def document_exists(doc_hash):
    results = client.scroll(
        collection_name=COLLECTION_NAME,
        scroll_filter=Filter(
            must=[
                FieldCondition(key="hash", match=MatchValue(value=doc_hash))
            ]
        ),
        limit=1
    )
    return len(results[0]) > 0

def add_to_vector_store(chunks, embeddings, filename, doc_hash, overwrite=False):
    if not overwrite and document_exists(doc_hash):
        raise ValueError("Duplicate document detected")

    timestamp = datetime.utcnow().isoformat()
    points = [
        PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": chunk,
                "filename": filename,
                "hash": doc_hash,
                "uploaded_at": timestamp,
                "source": "upload"
            }
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
