from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


class TelemetryService:
    def __init__(self, telemetry_file: Path) -> None:
        self.telemetry_file = telemetry_file

    def read_events(self, limit: int = 200) -> list[dict[str, Any]]:
        if not self.telemetry_file.exists():
            return []

        rows = self.telemetry_file.read_text(encoding="utf-8").splitlines()[-limit:]
        events: list[dict[str, Any]] = []
        for line in rows:
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return events

    def summarize(self, limit: int = 400) -> dict[str, Any]:
        events = self.read_events(limit)
        counter = Counter(e.get("event", "unknown") for e in events)
        providers = Counter(
            e.get("payload", {}).get("provider", "n/a")
            for e in events
            if e.get("event") == "llm.reply"
        )
        risks = Counter(
            e.get("payload", {}).get("risk_level", "n/a")
            for e in events
            if e.get("event") == "llm.reply"
        )

        return {
            "event_count": len(events),
            "top_events": counter.most_common(10),
            "providers": dict(providers),
            "risk_levels": dict(risks),
            "latest": events[-20:],
        }
