from __future__ import annotations

from openai import OpenAI


class OpenAIBackend:
    def __init__(self, api_key: str, model: str) -> None:
        self.client = OpenAI(api_key=api_key)
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
