from fastapi import FastAPI, UploadFile, File, HTTPException
from routers import upload, search

app = FastAPI(title="Bert3 Knowledge API")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(search.router, prefix="/search", tags=["Search"])

@app.get("/")
def root():
    return {"status": "Bert3 Knowledge API is running."}
