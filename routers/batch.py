from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile
import os
import asyncio
import logging

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store, compute_hash

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []

    # Read files into memory while still in request context
    file_data = []
    for file in files:
        try:
            content = await file.read()
            file_data.append((file.filename, content))
        except Exception as e:
            results.append({"file": file.filename, "error": f"read failure: {str(e)}"})

    async def process_file(filename, contents):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(contents)
                tmp_path = tmp.name

            with open(tmp_path, "rb") as f:
                text = f.read().decode("utf-8", errors="ignore")

            os.remove(tmp_path)

            if not text.strip():
                raise ValueError("No text content extracted from file")

            chunks = chunk_text(text)
            if not chunks:
                raise ValueError("Text was extracted but chunking returned no results")

            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(text)

            add_to_vector_store(
                embeddings,
                metadata={"filename": filename, "hash": doc_hash},
                overwrite=overwrite
            )

            logger.info(f"✅ Uploaded: {filename}")
            return {"file": filename, "status": "uploaded"}

        except Exception as e:
            logger.error(f"❌ Error: {filename} | {str(e)}")
            return {"file": filename, "error": str(e)}

    # Process files concurrently
    upload_tasks = [
        process_file(filename, contents)
        for filename, contents in file_data
    ]

    results += await asyncio.gather(*upload_tasks)

    return {"status": "completed", "results": results}
