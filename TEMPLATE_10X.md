# Jarvis 10x Repo Template (Professional)

## Included
- `run.py`: core + api process supervisor
- `core/main.py`: REPL runtime shell
- `api/server.py`: FastAPI service (`/`, `/health`, `/status`, `/metrics`, `/dashboard`)
- `api/telemetry_service.py`: telemetry parsing + aggregate metrics service
- `api/static/dashboard.html`: Mission Control visual panel
- `jarvis/jarvis/agents.py`: Planner + Safety + Persona agent orchestration
- `tests/`: pytest smoke coverage for agents + telemetry summarization
- `requirements.txt`: runtime + build + test dependencies
- `.github/workflows/build.yml`: Windows build + artifact upload

## Local run
```bash
pip install -r requirements.txt
python run.py
```

Open:
- `http://127.0.0.1:8000/dashboard` (Mission Control)
- `http://127.0.0.1:8000/metrics` (JSON telemetry)
- `http://127.0.0.1:8000/status` (runtime overview)

## Run tests
```bash
pytest -q
```

## Build locally
```bash
pyinstaller run.py --onefile --name Jarvis
```

## GitHub Actions artifact
Workflow tamamlandığında Actions > build > Artifacts altında `Jarvis.exe` indirilebilir.
