from __future__ import annotations

import datetime as dt
import subprocess
import webbrowser


class CommandRouter:
    """Beyaz liste komut çalıştırıcı."""

    def __init__(self) -> None:
        self.allowed = {
            "not defteri": self.open_notepad,
            "youtube": self.open_youtube,
            "saat kaç": self.tell_time,
        }

    def handle(self, text: str) -> str | None:
        lowered = text.lower()
        for key, fn in self.allowed.items():
            if key in lowered:
                return fn()
        return None

    @staticmethod
    def open_notepad() -> str:
        subprocess.Popen(["notepad.exe"])
        return "Not defteri açıldı."

    @staticmethod
    def open_youtube() -> str:
        webbrowser.open("https://www.youtube.com")
        return "YouTube açıldı."

    @staticmethod
    def tell_time() -> str:
        now = dt.datetime.now().strftime("%H:%M")
        return f"Şu an saat {now}."
