from fastapi import APIRouter, UploadFile, File, Query
from typing import List
import tempfile
import os
import asyncio

from services.chunking import chunk_text  # ✅ CORRECT FUNCTION
from services.embeddings import embed_chunks
from vector_store import upsert_vectors, compute_hash

router = APIRouter()

@router.post("/batch_upload/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(default=False)
):
    results = []

    # Read all file contents up front
    file_data = []
    for file in files:
        try:
            content = await file.read()
            file_data.append((file.filename, content))
        except Exception as e:
            results.append({
                "file": file.filename,
                "status": "❌ Failed to read",
                "error": str(e)
            })

    async def process_file(filename, contents):
        try:
            import fitz  # ✅ Using PyMuPDF directly here

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(contents)
                tmp_path = tmp.name

            # Extract text using fitz
            doc = fitz.open(tmp_path)
            full_text = " ".join([page.get_text() for page in doc])
            doc.close()

            os.remove(tmp_path)

            # Chunk and embed
            chunks = chunk_text(full_text)
            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(full_text)

            # Store
            upsert_vectors(chunks, embeddings, filename, doc_hash, overwrite=overwrite)

            return {
                "file": filename,
                "status": "✅ Uploaded"
            }

        except ValueError as ve:
            return {
                "file": filename,
                "status": "⚠️ Skipped (Duplicate)",
                "error": str(ve)
            }
        except Exception as e:
            return {
                "file": filename,
                "status": "❌ Failed",
                "error": str(e)
            }

    # Run all uploads concurrently
    tasks = [process_file(fn, data) for fn, data in file_data]
    results += await asyncio.gather(*tasks)

    return {
        "status": "complete",
        "results": results,
        "summary": {
            "uploaded": [r["file"] for r in results if r["status"].startswith("✅")],
            "skipped": [r["file"] for r in results if r["status"].startswith("⚠️")],
            "failed": [r["file"] for r in results if r["status"].startswith("❌")]
        }
    }
