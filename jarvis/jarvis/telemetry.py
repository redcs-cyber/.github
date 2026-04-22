from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class TelemetryEvent:
    ts: float
    level: str
    event: str
    payload: dict[str, Any]


class Telemetry:
    def __init__(self, path: str = "telemetry/events.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, event: str, payload: dict[str, Any] | None = None, level: str = "info") -> None:
        row = TelemetryEvent(
            ts=time.time(),
            level=level,
            event=event,
            payload=payload or {},
        )
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")
