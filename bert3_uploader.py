## bert3_uploader.py

import os
import argparse
import httpx
import fitz  # PyMuPDF
import hashlib
from pathlib import Path
from datetime import datetime

API_URL = os.getenv("BERT3_API_URL", "http://localhost:10000")
UPLOAD_ENDPOINT = f"{API_URL}/upload/"
HEADERS = {"accept": "application/json"}


def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = "\n".join([page.get_text() for page in doc])
    return text


def compute_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def upload_file(file_path, api_url, overwrite=False):
    text = extract_text_from_pdf(file_path)
    doc_hash = compute_hash(text)
    filename = Path(file_path).name

    metadata = {
        "filename": filename,
        "hash": doc_hash,
        "uploaded_at": datetime.utcnow().isoformat(),
        "source": "cli"
    }

    files = {"file": (filename, text.encode("utf-8"))}
    try:
        response = httpx.post(api_url, files=files, headers=HEADERS, params={"overwrite": str(overwrite).lower()})
        response.raise_for_status()
        print(f"✅ Uploaded: {filename} | chunks: {response.json().get('chunks')}")
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 409:
            print(f"⚠️ Skipped duplicate: {filename}")
        else:
            print(f"❌ Failed to upload {filename}: {exc}")


def batch_upload(folder_path, api_url, overwrite):
    pdf_files = list(Path(folder_path).rglob("*.pdf"))
    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"\n📦 Uploading {len(pdf_files)} files to {api_url}\n")
    for file_path in pdf_files:
        upload_file(file_path, api_url, overwrite)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bert3 PDF Uploader CLI")
    parser.add_argument("--folder", required=True, help="Folder with PDF files")
    parser.add_argument("--api", default=UPLOAD_ENDPOINT, help="API endpoint to upload to")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing documents")

    args = parser.parse_args()
    batch_upload(args.folder, args.api, args.overwrite)
