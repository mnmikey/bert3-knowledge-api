from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import upsert_vectors, compute_hash
import fitz
from typing import List

router = APIRouter()


def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        content = file.file.read()
        doc = fitz.open(stream=content, filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")


@router.post("/")
async def batch_upload(
    files: List[UploadFile] = File(...),
    overwrite: bool = Query(False)
):
    results = {"uploaded": [], "skipped": [], "errors": []}

    for file in files:
        try:
            text = extract_text(file)
            chunks = chunk_text(text)
            embeddings = embed_chunks(chunks)
            doc_hash = compute_hash(text)
            upsert_vectors(chunks, embeddings, filename=file.filename, doc_hash=doc_hash, overwrite=overwrite)
            results["uploaded"].append(file.filename)
        except ValueError:
            results["skipped"].append(file.filename)
        except Exception as e:
            results["errors"].append({"file": file.filename, "error": str(e)})

    return results
