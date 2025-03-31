from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile
import os
import asyncio
from services.chunking import chunk_pdf_file
from services.embeddings import embed_chunks
from vector_store import store_embeddings

router = APIRouter()

@router.post("/batch_upload/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []

    # Read all file contents first while request context is still open
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

            chunks = chunk_pdf_file(tmp_path)
            embeddings = embed_chunks(chunks)
            store_embeddings(embeddings, metadata={"filename": filename}, overwrite=overwrite)

            os.remove(tmp_path)
            return {"file": filename, "status": "uploaded"}
        except Exception as e:
            return {"file": filename, "error": str(e)}

    # Run file uploads concurrently
    upload_tasks = [
        process_file(filename, contents)
        for filename, contents in file_data
    ]

    results += await asyncio.gather(*upload_tasks)

    return {"status": "accepted", "results": results}
