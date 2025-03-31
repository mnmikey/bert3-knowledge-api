from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile, os, asyncio

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
            text = content.decode("utf-8", errors="ignore")
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(text)

            upsert_vectors(chunks, embeddings, file.filename, doc_hash, overwrite=overwrite)

            return {"file": file.filename, "status": "uploaded"}
        except Exception as e:
            return {"file": file.filename, "error": str(e)}

    tasks = [process_file(file) for file in files]
    return {"status": "accepted", "results": await asyncio.gather(*tasks)}
