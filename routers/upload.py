from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import upsert_vectors, compute_hash

router = APIRouter()

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    overwrite: bool = Query(False)
):
    text = (await file.read()).decode("utf-8")
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    doc_hash = compute_hash(text)

    try:
        upsert_vectors(chunks, embeddings, filename=file.filename, doc_hash=doc_hash, overwrite=overwrite)
    except ValueError:
        raise HTTPException(status_code=409, detail="Duplicate document. Use ?overwrite=true to replace.")

    return {"status": "uploaded", "chunks": len(chunks)}
