from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile
import os
import asyncio
import logging

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store

router = APIRouter()

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def log_event(message: str):
    logging.info(message)


# --- Optional future memory hook ---
#def store_to_memory(*args, **kwargs):
#    pass  # 🔜 Stubbed out for future memory integration


@router.post("/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []
    file_data = []

    # --- Pre-read file contents (avoids closed file handles) ---
    for file in files:
        try:
            content = await file.read()
            file_data.append((file.filename, content))
        except Exception as e:
            msg = f"❌ Read failure: {file.filename} | {str(e)}"
            log_event(msg)
            results.append({"file": file.filename, "error": str(e)})

    # --- Async handler for each file ---
    async def process_file(filename, contents):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(contents)
                tmp_path = tmp.name

            # Extract + embed + store
            chunks = chunk_text(tmp_path)
            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(contents)
            add_to_vector_store(embeddings, filename, doc_hash, overwrite=overwrite)

            os.remove(tmp_path)

            log_event(f"✅ Uploaded: {filename}")
            return {"file": filename, "status": "uploaded"}

        except Exception as e:
            log_event(f"❌ Error: {filename} | {str(e)}")
            return {"file": filename, "error": str(e)}

    # --- Run all uploads concurrently ---
    upload_tasks = [process_file(fn, data) for fn, data in file_data]
    results += await asyncio.gather(*upload_tasks)

    return {"status": "accepted", "results": results}
