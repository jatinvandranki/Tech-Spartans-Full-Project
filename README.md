# Tech Spartans - Full Hackathon Demo Project

This is a ready-to-run demo for the hackathon. It provides:
- simple baseline candidate generation (frequency-based)
- a lightweight Markov chain generator for more creative guesses
- a Python MD5 "cracker" (for demo purposes, no Hashcat required)
- a FastAPI backend and Streamlit frontend

## Quick Start (for absolute beginners)

1. Download/unzip this project.
2. Open a terminal in the project folder.
3. Create a Python virtual environment and activate it:

On Windows (PowerShell):
```
python -m venv venv
.\venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

On macOS/Linux (bash):
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Prepare dataset (run once):
```
python scripts/clean_dataset.py
python scripts/generate_candidates_baseline.py
python scripts/generate_markov.py
```

5. Run backend (in one terminal):
```
uvicorn backend.main:app --reload --port 8000
```

6. Run frontend (in another terminal):
```
streamlit run frontend/app.py
```

7. Demo cracking locally using sample hashes (optional):
```
python scripts/crack_hashes.py hashes/sample_md5.txt candidates/top100k.txt
```

## Who should run what (simple instructions)

- **Jatin (Leader)**: Start backend and explain steps to team.
- **Vikas (AI)**: Run `scripts/clean_dataset.py` and `scripts/generate_markov.py` to produce candidates.
- **Saran (Backend)**: Start backend `uvicorn backend.main:app --reload --port 8000`
- **Vivek (Frontend)**: Start Streamlit `streamlit run frontend/app.py` and demo UI
- **Harsh (Security)**: Run `python scripts/crack_hashes.py hashes/sample_md5.txt candidates/top100k.txt` and verify cracked results

## Notes
- This demo uses Python MD5 checks to emulate cracking for the hackathon presentation. If you want to use Hashcat later, you can, but for demo reliability across systems this Python method is easier.
- Keep candidate lists small during demo to be fast (Top N set in UI).
