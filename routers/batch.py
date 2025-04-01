from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile, os, asyncio, logging

from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store

router = APIRouter()

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
