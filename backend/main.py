from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import uvicorn, os, asyncio, hashlib, json, time, shutil
from typing import List
import subprocess

app = FastAPI()

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(BASE, ".."))

def read_candidates(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [l.strip() for l in f if l.strip()]

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/predict")
def predict(type: str = "baseline", top_n: int = 200):
    root = os.path.abspath(os.path.join(BASE, ".."))
    if type == "baseline":
        path = os.path.join(root, "candidates", "top100k.txt")
        candidates = read_candidates(path)[:top_n]
    elif type == "markov":
        path = os.path.join(root, "candidates", "markov_top.txt")
        candidates = read_candidates(path)[:top_n]
    else:
        candidates = ["password123","123456","qwerty"]
    return {"candidates": candidates}

@app.post("/crack")
async def crack(hashfile: UploadFile = File(...), predictor: str = Form("baseline"), top_n: int = Form(1000)):
    # Save uploaded file
    temp_dir = os.path.join(ROOT, "hashes", "uploads")
    os.makedirs(temp_dir, exist_ok=True)
    dest = os.path.join(temp_dir, hashfile.filename)
    with open(dest, "wb") as f:
        f.write(await hashfile.read())

    # Read hashes (expecting lines like: md5hash[:plaintext])
    with open(dest, "r") as f:
        lines = [l.strip() for l in f if l.strip()]
    hashes = []
    for l in lines:
        if ":" in l:
            h, _ = l.split(":",1)
            hashes.append(h.strip())
        else:
            hashes.append(l.strip())

    # Get candidates from predict endpoint logic
    candidates_resp = predict(type=predictor, top_n=top_n)
    candidates = candidates_resp["candidates"]

    # Simple MD5 cracking in Python (no Hashcat required)
    results = {}
    start = time.time()
    md5_to_plain = {}
    cand_count = 0
    for cand in candidates:
        cand_count += 1
        h = hashlib.md5(cand.encode("utf-8", errors="ignore")).hexdigest()
        if h in hashes:
            md5_to_plain[h] = cand
    duration = time.time() - start

    # Build response
    cracked = []
    for h in hashes:
        cracked.append({"hash": h, "password": md5_to_plain.get(h, None)})

    return {"cracked": cracked, "duration_seconds": duration, "candidates_tried": cand_count}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
