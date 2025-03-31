from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile, os, asyncio, traceback

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import upsert_vectors, compute_hash

router = APIRouter()

@router.post("/batch_upload/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []

    async def process_file(file: UploadFile):
        try:
            content = await file.read()
            if not content:
                return {"file": file.filename, "status": "error", "error": "Empty file"}

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                raw_text = f.read().decode("latin1")  # fallback if UTF-8 fails

            chunks = chunk_text(raw_text)
            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(raw_text)

            upsert_vectors(chunks, embeddings, file.filename, doc_hash, overwrite)
            os.remove(tmp_path)

            return {"file": file.filename, "status": "uploaded"}

        except Exception as e:
            return {
                "file": file.filename,
                "status": "error",
                "error": str(e),
                "traceback": traceback.format_exc()
            }

    upload_tasks = [process_file(file) for file in files]
    results = await asyncio.gather(*upload_tasks)

    return {
        "status": "completed",
        "files_processed": len(results),
        "results": results
    }
