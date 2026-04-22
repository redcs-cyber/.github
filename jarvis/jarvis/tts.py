from __future__ import annotations

import subprocess
from pathlib import Path

import sounddevice as sd
import soundfile as sf


class PiperTTS:
    def __init__(self, piper_exe: str, model_path: str, output_wav: str) -> None:
        self.piper_exe = piper_exe
        self.model_path = model_path
        self.output_wav = output_wav

    def speak(self, text: str) -> None:
        if not self.model_path:
            print(f"[TTS] {text}")
            return

        out_path = Path(self.output_wav)
        cmd = [
            self.piper_exe,
            "--model",
            self.model_path,
            "--output_file",
            str(out_path),
        ]
        subprocess.run(cmd, input=text, text=True, check=True)
        data, sr = sf.read(out_path, dtype="float32")
        sd.play(data, sr)
        sd.wait()
