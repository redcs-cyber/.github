from __future__ import annotations

import requests


class OllamaBackend:
    def __init__(self, url: str, model: str) -> None:
        self.url = url
        self.model = model

    def reply(self, prompt: str, system: str = "") -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system or "Kısa ve net cevap ver."},
                {"role": "user", "content": prompt},
            ],
        }
        r = requests.post(self.url, json=payload, timeout=90)
        r.raise_for_status()
        data = r.json()
        return data.get("message", {}).get("content", "")
