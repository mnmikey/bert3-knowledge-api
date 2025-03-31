from fastapi import APIRouter, UploadFile, File, HTTPException, Query, BackgroundTasks
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import upsert_vectors, compute_hash
import fitz
from typing import List
import traceback
import tempfile
import os

router = APIRouter()


def extract_text_from_pdf(path: str):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])


@router.post("/")
async def batch_upload(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(False)
):
    for file in files:
        background_tasks.add_task(process_file, file, overwrite)
    return {"status": "accepted", "queued_files": [f.filename for f in files]}


def process_file(file: UploadFile, overwrite: bool):
    try:
        print(f"📄 Queued: {file.filename}")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(file.file.read())
            tmp_path = tmp.name

        file.file.close()

        text = extract_text_from_pdf(tmp_path)
        chunks = chunk_text(text)
        print(f"🔹 {file.filename} → {len(chunks)} chunks")

        if not chunks:
            raise ValueError("No chunks generated from file.")

        embeddings = embed_chunks(chunks)
        print(f"🔸 {file.filename} → {len(embeddings)} embeddings")

        doc_hash = compute_hash(text)
        upsert_vectors(chunks, embeddings, filename=file.filename, doc_hash=doc_hash, overwrite=overwrite)
        print(f"✅ Upserted {len(embeddings)} to Qdrant for: {file.filename}")

        os.remove(tmp_path)
    except Exception as e:
        tb = traceback.format_exc()
        print(f"❌ Error processing {file.filename}: {e}\n{tb}")
