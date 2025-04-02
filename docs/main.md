# 🧠 `main.py` – Bert3 Knowledge API Entry Point

This script serves as the **main bootloader** for the Bert3 Knowledge API.

It initializes the FastAPI server and connects the key API endpoints:

- `/upload` → Handles single file ingestion via `upload.py`
- `/search` → Handles semantic search queries via `search.py`
- `/batch_upload` → Supports bulk upload of multiple files via `batch.py`

---

## 🧩 Modules & Structure

```python
from fastapi import FastAPI
from routers import upload, search, batch
```

The `FastAPI()` instance is configured and routes are modularly included for clean separation of concerns:

```python
app = FastAPI(title="Bert3 Knowledge API")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(batch.router, prefix="/batch_upload", tags=["Batch"])
```

A simple root route returns a health check/status response:

```python
@app.get("/")
def root():
    return {"status": "Bert3 Knowledge API is running."}
```

---

## ⚙️ Runtime Behavior

- Initializes FastAPI app instance with custom title
- Modularly registers 3 routers (`upload`, `search`, `batch`)
- Exposes a root-level `/` route to validate that the service is up and reachable

---

## 🏷 Tags & Metadata

- **Type**: Entry Point
- **Purpose**: FastAPI init and router setup
- **Tags**: `api`, `bootloader`, `routing`
