# Jarvis 10x Repo Template

## Included
- `run.py`: core + api orchestrator
- `core/main.py`: interactive assistant loop
- `api/server.py`: FastAPI endpoints (`/`, `/health`)
- `requirements.txt`: runtime + build dependencies
- `.github/workflows/build.yml`: Windows build + artifact upload

## Local run
```bash
pip install -r requirements.txt
python run.py
```

## Build locally
```bash
pyinstaller run.py --onefile --name Jarvis
```

## GitHub Actions artifact
Workflow tamamlandığında Actions > build > Artifacts altında `Jarvis.exe` indirilebilir.
