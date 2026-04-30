from __future__ import annotations

import numpy as np
import sounddevice as sd


def record_chunk(sample_rate: int, seconds: int) -> np.ndarray:
    frames = int(sample_rate * seconds)
    audio = sd.rec(frames, samplerate=sample_rate, channels=1, dtype="float32")
    sd.wait()
    return audio.flatten()
