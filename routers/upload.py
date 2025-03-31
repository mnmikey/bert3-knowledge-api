from fastapi import APIRouter, UploadFile, File
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import upsert_vectors

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    text = (await file.read()).decode("utf-8")
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    upsert_vectors(chunks, embeddings)
    return {"status": "uploaded", "chunks": len(chunks)}
