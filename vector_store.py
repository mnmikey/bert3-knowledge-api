import hashlib
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
import uuid
import logging

client = QdrantClient(":memory:")

COLLECTION_NAME = "bert3-docs"

def compute_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def add_to_vector_store(vectors, metadata_list, overwrite=False):
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE)
        )

    points = []
    for vec, meta in zip(vectors, metadata_list):
        uid = str(uuid.uuid4())
        points.append(PointStruct(id=uid, vector=vec, payload=meta))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    logging.info(f"✅ Stored {len(points)} vectors in Qdrant.")
