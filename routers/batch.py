from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile
import os
import asyncio
import fitz  # PyMuPDF
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store  # ✅ Corrected import

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
                tmp.flush()
                tmp_path = tmp.name

            # Extract text with PyMuPDF
            doc = fitz.open(tmp_path)
            text = "\n".join([page.get_text() for page in doc])

            # Chunk, embed, store
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            add_to_vector_store(  # ✅ Corrected call
                file_path=filename,
                chunks=chunks,
                embeddings=embeddings,
                overwrite=overwrite
            )

            os.remove(tmp_path)
            return {"file": filename, "status": "uploaded"}
        except Exception as e:
            return {"file": filename, "error": str(e)}

    upload_tasks = [process_file(filename, contents) for filename, contents in file_data]
    results += await asyncio.gather(*upload_tasks)

    return {"status": "accepted", "results": results}
