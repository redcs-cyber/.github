from __future__ import annotations

import numpy as np


class WhisperSTT:
    def __init__(self, model_name: str, device: str, compute_type: str) -> None:
        from faster_whisper import WhisperModel

        self.model = WhisperModel(model_name, device=device, compute_type=compute_type)

    def transcribe(self, audio: np.ndarray, sample_rate: int = 16000) -> str:
        segments, _ = self.model.transcribe(audio, language="tr", vad_filter=True)
        return " ".join(s.text.strip() for s in segments).strip()
