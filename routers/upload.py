from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store, compute_hash
import fitz  # PyMuPDF
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

def extract_text(file: UploadFile):
    if file.filename.endswith(".pdf"):
        try:
            content = file.file.read()
            doc = fitz.open(stream=content, filetype="pdf")
            text = "\n".join([page.get_text() for page in doc])
            return text
        except Exception as e:
            logger.error(f"PDF extract failed: {e}")
            raise HTTPException(status_code=400, detail="Error extracting text from PDF.")
    elif file.filename.endswith(".txt"):
        return file.file.read().decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Only .pdf and .txt allowed.")

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    overwrite: bool = Query(False),
):
    try:
        text = extract_text(file)
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Extracted text is empty.")
        
        chunks = chunk_text(text)
        embeddings = embed_chunks(chunks)
        doc_hash = compute_hash(text)

        add_to_vector_store(
            chunks,
            embeddings,
            filename=file.filename,
            doc_hash=doc_hash,
            overwrite=overwrite,
        )

        return {"status": "uploaded", "chunks": len(chunks)}

    except Exception as e:
        logger.exception("❌ Upload failed")
        raise HTTPException(status_code=500, detail=str(e))
