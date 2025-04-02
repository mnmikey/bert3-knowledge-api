# 🧠 `batch.py` – Asynchronous Batch Upload Router

This script handles **multi-file asynchronous ingestion** for the Bert3 Knowledge API using FastAPI’s `UploadFile` interface.

It supports uploading **multiple `.pdf` or `.txt` files** in a single request and pushes them through the full ingestion pipeline: chunk → embed → store in Qdrant.

---

## 🧩 Modules & Structure

```python
from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile, os, asyncio, logging

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store
```

---

## 🔄 Upload Flow

```python
@router.post("/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []

    file_data = []
    for file in files:
        try:
            content = await file.read()
            file_data.append((file.filename, content.decode('utf-8', errors='ignore')))
        except Exception as e:
            results.append({"file": file.filename, "error": f"read failure: {str(e)}"})

    async def process_file(filename, content):
        try:
            logging.info(f"📄 Processing: {filename}")

            chunks = chunk_text(content)
            if not chunks:
                return {"file": filename, "error": "No chunks generated."}

            embeddings = embed_chunks(chunks)
            if not embeddings:
                return {"file": filename, "error": "Embedding generation failed."}

            metadata = [{"filename": filename, "chunk_index": idx} for idx in range(len(embeddings))]
            add_to_vector_store(embeddings, metadata, overwrite=overwrite)

            return {"file": filename, "status": "uploaded", "chunks": len(chunks)}
        except Exception as e:
            return {"file": filename, "error": str(e)}

    tasks = [process_file(fname, content) for fname, content in file_data]
    results += await asyncio.gather(*tasks)

    return {"status": "done", "results": results}
```

---

## ⚙️ Runtime Behavior

- Accepts multiple file uploads via `UploadFile`
- Processes all files asynchronously with `asyncio.gather`
- Handles chunking, embedding, and storing in parallel
- Returns summary of success/failure per file

---

## 🏷 Tags & Metadata

- **Type**: Router  
- **Purpose**: Multi-file ingestion → NLP pipeline → vector store  
- **Tags**: `batch`, `upload`, `router`, `async`, `embedding`, `pipeline`, `semantic`
