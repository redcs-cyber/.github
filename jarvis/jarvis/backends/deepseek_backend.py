from __future__ import annotations

from openai import OpenAI


class DeepSeekBackend:
    """DeepSeek OpenAI-compatible backend."""

    def __init__(self, api_key: str, model: str, base_url: str) -> None:
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def reply(self, prompt: str, system: str = "") -> str:
        rsp = self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system or "Kısa ve net cevap ver."},
                {"role": "user", "content": prompt},
            ],
        )
        return rsp.output_text
