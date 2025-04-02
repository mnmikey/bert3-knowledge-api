# 🧠 `upload.py` – Single File Upload Router

This script handles single PDF or TXT file ingestion for the Bert3 Knowledge API.

It processes the file through a modular ingestion pipeline:
- Extracts raw text from uploaded `.pdf` or `.txt`
- Chunks the text into token-aware segments
- Embeds each chunk using the OpenAI Embedding API
- Pushes the embeddings and metadata into Qdrant for semantic search

---

## 🧩 Modules & Structure

```python
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from services.chunking import chunk_text
from services.embeddings import embed_chunks
from vector_store import add_to_vector_store, compute_hash
import fitz  # PyMuPDF
import logging
```

The route is exposed via `POST /upload` and uses FastAPI's `UploadFile` for efficient streaming and decoding.

---

## 📄 Endpoint Logic

```python
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
```

---

## 📦 File Extraction Logic

```python
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
```

---

## ⚙️ Runtime Behavior

- Accepts uploaded `.pdf` or `.txt` file
- Extracts text based on file type
- Tokenizes text into manageable chunks
- Generates embeddings with OpenAI
- Pushes data to Qdrant vector DB via `add_to_vector_store`

---

## 🏷 Tags & Metadata

- **Type**: Router  
- **Purpose**: Single file upload → NLP pipeline → vector store  
- **Tags**: `upload`, `router`, `embedding`, `chunking`, `vector`, `semantic`, `pipeline`
