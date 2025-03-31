from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Form
from typing import List
import tempfile
import os
from services.chunking import chunk_pdf_file
from services.embeddings import embed_chunks
from vector_store import upsert_documents
import hashlib

router = APIRouter()


@router.post("/batch_upload")
async def batch_upload(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    overwrite: bool = Form(False)
):
    for file in files:
        background_tasks.add_task(process_file, file, overwrite)
    return {"status": "accepted", "queued_files": [f.filename for f in files]}


def process_file(file: UploadFile, overwrite: bool):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        file.file.close()

        chunks = chunk_pdf_file(tmp_path)
        embeddings = embed_chunks(chunks)

        file_hash = hashlib.sha256(file.filename.encode()).hexdigest()

        payloads = []
        for i, chunk in enumerate(chunks):
            payload = {
                "file_name": file.filename,
                "file_hash": file_hash,
                "chunk_index": i,
                "text": chunk,
            }
            payloads.append(payload)

        upsert_documents(embeddings, payloads, overwrite=overwrite)
        os.remove(tmp_path)
    except Exception as e:
        print(f"❌ Failed to process {file.filename}: {e}")
