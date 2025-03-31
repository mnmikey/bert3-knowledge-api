from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import upsert_vectors, compute_hash
import fitz  # PyMuPDF

router = APIRouter()


def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        # Read binary and parse PDF with fitz
        content = file.file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only .pdf and .txt allowed.")


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    overwrite: bool = Query(False)
):
    text = extract_text(file)
    chunks = chunk_text(text)
    embeddings = embed_chunks(chunks)
    doc_hash = compute_hash(text)

    try:
        upsert_vectors(chunks, embeddings, filename=file.filename, doc_hash=doc_hash, overwrite=overwrite)
    except ValueError:
        raise HTTPException(status_code=409, detail="Duplicate document. Use ?overwrite=true to replace.")

    return {"status": "uploaded", "chunks": len(chunks)}
