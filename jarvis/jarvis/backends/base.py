from __future__ import annotations

from typing import Protocol


class ChatBackend(Protocol):
    def reply(self, prompt: str, system: str = "") -> str:
        ...
