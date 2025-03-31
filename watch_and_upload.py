import os
import time
import argparse
import httpx
from pathlib import Path
from datetime import datetime

SUPPORTED_EXTENSIONS = [".pdf", ".txt"]
STATE_FILE = ".upload_state.txt"


def get_tracked_files(folder):
    return sorted([f for f in Path(folder).rglob("*") if f.suffix.lower() in SUPPORTED_EXTENSIONS])

def load_previous_hashes():
    if not os.path.exists(STATE_FILE):
        return set()
    with open(STATE_FILE, "r") as f:
        return set([line.strip() for line in f.readlines()])

def save_hashes(hashes):
    with open(STATE_FILE, "w") as f:
        f.write("\n".join(hashes))

def upload_files(files, api_url, overwrite):
    if not files:
        return
    files_to_send = [("files", (f.name, open(f, "rb"))) for f in files]
    response = httpx.post(
        api_url,
        files=files_to_send,
        params={"overwrite": str(overwrite).lower()}
    )
    print(f"[{datetime.now().isoformat()}] ✅ Uploaded batch: {[f.name for f in files]} | Status: {response.status_code}")
    print(response.json())


def main(folder, api_url, interval, overwrite):
    print(f"👀 Watching: {folder}\n🧠 Sending to: {api_url}\n⏱ Interval: {interval}s\n")
    seen = load_previous_hashes()

    while True:
        files = get_tracked_files(folder)
        new_files = [f for f in files if str(f.resolve()) not in seen]

        if new_files:
            try:
                upload_files(new_files, api_url, overwrite)
                seen.update(str(f.resolve()) for f in new_files)
                save_hashes(seen)
            except Exception as e:
                print(f"❌ Upload failed: {e}")

        time.sleep(interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-upload watcher for Bert3")
    parser.add_argument("--watch_folder", required=True, help="Folder to monitor for PDFs/TXTs")
    parser.add_argument("--api", required=True, help="/batch_upload endpoint URL")
    parser.add_argument("--interval", type=int, default=30, help="Polling interval in seconds")
    parser.add_argument("--overwrite", action="store_true", help="Force overwrite if duplicate")
    args = parser.parse_args()

    main(args.watch_folder, args.api, args.interval, args.overwrite)
