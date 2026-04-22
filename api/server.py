from __future__ import annotations

import json
import os
from collections import Counter
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI(title="Jarvis API", version="2.0.0")

TELEMETRY_FILE = Path(os.getenv("TELEMETRY_FILE", "jarvis/telemetry/events.jsonl"))


def _read_events(limit: int = 200) -> list[dict]:
    if not TELEMETRY_FILE.exists():
        return []
    rows = TELEMETRY_FILE.read_text(encoding="utf-8").splitlines()[-limit:]
    events = []
    for line in rows:
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return events


@app.get("/")
def home():
    return {"ok": True, "service": "jarvis-api", "dashboard": "/dashboard"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/metrics")
def metrics():
    events = _read_events(400)
    counter = Counter(e.get("event", "unknown") for e in events)
    providers = Counter(
        e.get("payload", {}).get("provider", "n/a")
        for e in events
        if e.get("event") == "llm.reply"
    )
    risk = Counter(
        e.get("payload", {}).get("risk_level", "n/a")
        for e in events
        if e.get("event") == "llm.reply"
    )
    return {
        "event_count": len(events),
        "top_events": counter.most_common(10),
        "providers": providers,
        "risk_levels": risk,
        "latest": events[-20:],
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return Path("api/static/dashboard.html").read_text(encoding="utf-8")


if __name__ == "__main__":
    uvicorn.run("api.server:app", host="0.0.0.0", port=8000, reload=False)
