from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

from api.telemetry_service import TelemetryService

app = FastAPI(title="Jarvis API", version="2.1.0")

TELEMETRY_FILE = Path(os.getenv("TELEMETRY_FILE", "jarvis/telemetry/events.jsonl"))
service = TelemetryService(TELEMETRY_FILE)


@app.get("/")
def home():
    return {
        "ok": True,
        "service": "jarvis-api",
        "dashboard": "/dashboard",
        "metrics": "/metrics",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/status")
def status():
    summary = service.summarize(100)
    return {
        "telemetry_file": str(TELEMETRY_FILE),
        "event_count": summary["event_count"],
        "providers": summary["providers"],
    }


@app.get("/metrics")
def metrics():
    return service.summarize(400)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return Path("api/static/dashboard.html").read_text(encoding="utf-8")


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=False)
