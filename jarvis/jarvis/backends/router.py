from __future__ import annotations

from dataclasses import dataclass

from jarvis.backends.deepseek_backend import DeepSeekBackend
from jarvis.backends.ollama_backend import OllamaBackend
from jarvis.backends.openai_backend import OpenAIBackend


@dataclass
class ProviderResult:
    provider: str
    content: str


class MultiProviderRouter:
    def __init__(self, settings) -> None:
        self.chain: list[tuple[str, object]] = []

        for provider in settings.brain_providers:
            if provider == "ollama":
                self.chain.append((provider, OllamaBackend(settings.ollama_url, settings.ollama_model)))
            elif provider == "deepseek" and settings.deepseek_api_key:
                self.chain.append(
                    (
                        provider,
                        DeepSeekBackend(settings.deepseek_api_key, settings.deepseek_model, settings.deepseek_base_url),
                    )
                )
            elif provider == "openai" and settings.openai_api_key:
                self.chain.append((provider, OpenAIBackend(settings.openai_api_key, settings.openai_model, settings.openai_base_url)))

        if not self.chain:
            self.chain.append(("ollama", OllamaBackend(settings.ollama_url, settings.ollama_model)))

    def reply(self, prompt: str, system: str = "") -> ProviderResult:
        last_error = None
        for name, backend in self.chain:
            try:
                content = backend.reply(prompt, system)
                return ProviderResult(provider=name, content=content)
            except Exception as exc:
                last_error = exc
                continue
        raise RuntimeError(f"Tüm sağlayıcılar başarısız: {last_error}")
