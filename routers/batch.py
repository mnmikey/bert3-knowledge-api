from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile, os, asyncio, traceback

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store, compute_hash

from datetime import datetime
from kingbert_firestore_memory_onrender_com__jit_plugin import storeMemory

router = APIRouter()

@router.post("/batch_upload/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False),
):
    timestamp = datetime.utcnow().isoformat()
    session_id = "default"
    results = []

    async def process(file: UploadFile):
        temp_file_path = None
        try:
            suffix = os.path.splitext(file.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                temp_file_path = tmp.name
                tmp.write(await file.read())

            with open(temp_file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            chunks = chunk_text(content)
            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(content)

            add_to_vector_store(
                chunks=chunks,
                embeddings=embeddings,
                filename=file.filename,
                doc_hash=doc_hash,
                overwrite=overwrite,
                source="batch_upload"
            )

            result = {"filename": file.filename, "status": "✅ Success"}
        except Exception as e:
            result = {
                "filename": file.filename,
                "status": "❌ Error",
                "error": str(e),
                "trace": traceback.format_exc(),
            }
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return result

    results = await asyncio.gather(*[process(file) for file in files])

    # Firestore memory logging (asynchronous, non-blocking)
    try:
        await storeMemory({
            "session_id": session_id,
            "key": "batch_upload_log",
            "value": {
                "timestamp": timestamp,
                "results": results,
                "tags": ["upload", "batch", "log"]
            }
        })
    except Exception as log_err:
        print("⚠️ Firestore logging failed:", log_err)

    return {"results": results, "timestamp": timestamp}
