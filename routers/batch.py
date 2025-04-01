from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile
import os
import asyncio

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store

router = APIRouter()

@router.post("/batch_upload/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []

    # Step 1: Read all file contents while request context is active
    file_data = []
    for file in files:
        try:
            content = await file.read()
            file_data.append((file.filename, content))
        except Exception as e:
            results.append({"file": file.filename, "error": f"read failure: {str(e)}"})

    # Step 2: Process each file asynchronously
    async def process_file(filename, content_bytes):
        try:
            text = content_bytes.decode("utf-8", errors="ignore")
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)

            add_to_vector_store(
                embeddings,
                metadata={"filename": filename},
                overwrite=overwrite
            )

            print(f"✅ Uploaded {filename} | Chunks: {len(chunks)}")
            return {"file": filename, "status": "uploaded", "chunks": len(chunks)}
        except Exception as e:
            print(f"❌ Error uploading {filename}: {str(e)}")
            return {"file": filename, "error": str(e)}

    upload_tasks = [
        process_file(filename, content)
        for filename, content in file_data
    ]

    results += await asyncio.gather(*upload_tasks)
    return {"status": "accepted", "results": results}
