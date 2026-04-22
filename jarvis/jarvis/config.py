from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


@dataclass
class Settings:
    mode: str
    sample_rate: int
    chunk_seconds: int
    whisper_model: str
    whisper_device: str
    whisper_compute_type: str
    ollama_url: str
    ollama_model: str
    openai_api_key: str
    openai_model: str
    piper_exe: str
    piper_model: str
    piper_output_wav: str
    wakeword: str
    wakeword_model_path: str
    mcp_servers_file: str
    telemetry_file: str


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        mode=os.getenv("JARVIS_MODE", "local"),
        sample_rate=int(os.getenv("SAMPLE_RATE", "16000")),
        chunk_seconds=int(os.getenv("CHUNK_SECONDS", "3")),
        whisper_model=os.getenv("WHISPER_MODEL", "small"),
        whisper_device=os.getenv("WHISPER_DEVICE", "cpu"),
        whisper_compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8"),
        ollama_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        piper_exe=os.getenv("PIPER_EXE", "piper"),
        piper_model=os.getenv("PIPER_MODEL", ""),
        piper_output_wav=os.getenv("PIPER_OUTPUT_WAV", "out.wav"),
        wakeword=os.getenv("WAKEWORD", "jarvis"),
        wakeword_model_path=os.getenv("WAKEWORD_MODEL_PATH", ""),
        mcp_servers_file=os.getenv("MCP_SERVERS_FILE", "mcp_servers.json"),
        telemetry_file=os.getenv("TELEMETRY_FILE", "telemetry/events.jsonl"),
    )


def load_mcp_servers(path: str) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))
