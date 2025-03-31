from fastapi import FastAPI
from routers import upload, search, batch

app = FastAPI(title="Bert3 Knowledge API")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(batch.router, prefix="/batch_upload", tags=["Batch"])

@app.get("/")
def root():
    return {"status": "Bert3 Knowledge API is running."}
