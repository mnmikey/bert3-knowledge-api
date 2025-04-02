# 🧠 `vector_store.py` – Vector Database Interface

This script handles all Qdrant interactions for the **Bert3 Knowledge API**. It’s the primary interface for:

- Creating and managing the Qdrant collection
- Ingesting embedded document vectors
- Performing filtered semantic search

---

## 🧩 Modules & Structure

```python
import os
import uuid
import hashlib
import logging
from typing import List

import openai
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Filter, FieldCondition, MatchValue
from qdrant_client.http.models import Distance, VectorParams, SearchParams
```

---

## 🧠 Core Constants

```python
COLLECTION_NAME = "bert3_vector_store"
EMBEDDING_MODEL = "text-embedding-ada-002"
QDRANT_URL = os.environ.get("QDRANT_URL")
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")


Qdrant client is initialized securely via environment variables.

---

## 📦 Collection Management

Ensures Qdrant collection is initialized:

```python
def ensure_collection_exists():
    ...
```

- Recreates collection if not already present
- Uses 1536-dim cosine similarity (for Ada-002 embeddings)

---

## 🔐 Hashing Utility

Each chunk is hashed to ensure data integrity and deduplication:

```python
def compute_hash(text: str) -> str:
    return hashlib.md5(text.encode("utf-8")).hexdigest()
```

---

## 📤 Ingestion Flow

```python
def add_to_vector_store(chunks: List[str], metadata: dict):
    ...
```

- Chunks are embedded using OpenAI
- Payload includes: `text`, `doc_id`, `source`, and `hash`
- Data is upserted into Qdrant using `PointStruct`

---

## 🔍 Semantic Search

```python
def semantic_search(query: str, doc_id: str, top_k: int = 5) -> List[str]:
    ...
```

- Query is embedded with OpenAI
- Search is filtered by `doc_id`
- Returns top-k semantically similar chunks

---

## ⚙️ Runtime Behavior

- Initializes Qdrant client from env
- Handles chunk → embed → Qdrant pipeline
- Modular search with filter and limit control

---

## 🏷 Tags & Metadata

- **Type**: Store Layer
- **Purpose**: Qdrant ingestion/search interface
- **Tags**: `vectorstore`, `qdrant`, `search`, `embedding`, `semantic`, `filtering`, `openai`
