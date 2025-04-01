# vector_store.py

import hashlib
import os
import logging
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from openai import OpenAI
from uuid import uuid4

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "bert3_vector_store"

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

openai_client = OpenAI()

def ensure_collection_exists():
    """Ensures the Qdrant collection exists with the correct schema."""
    collections = client.get_collections().collections
    if not any(col.name == COLLECTION_NAME for col in collections):
        logger.info(f"Creating collection '{COLLECTION_NAME}'")
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
        )
    else:
        logger.info(f"Collection '{COLLECTION_NAME}' already exists")

ensure_collection_exists()

def compute_hash(text: str) -> str:
    """Create a SHA256 hash of a string (for deduplication)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def add_to_vector_store(chunks: list[dict], source: str):
    """Embed chunks and add them to Qdrant vector store."""
    vectors = []
    ids = []
    payloads = []

    for chunk in chunks:
        text = chunk["text"]
        doc_hash = compute_hash(text)
        try:
            embedding = openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            ).data[0].embedding
        except Exception as e:
            logger.error(f"Embedding failed for chunk: {e}")
            continue

        vectors.append(embedding)
        ids.append(str(uuid4()))
        payloads.append({
            "text": text,
            "source": source,
            "doc_hash": doc_hash
        })

    # Send to Qdrant
    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(id=id_, vector=vec, payload=pl)
                for id_, vec, pl in zip(ids, vectors, payloads)
            ]
        )
        logger.info(f"✅ Successfully added {len(vectors)} vectors to Qdrant.")
    except Exception as e:
        logger.error(f"❌ Failed to upsert into Qdrant: {e}")
