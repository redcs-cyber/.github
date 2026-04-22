from __future__ import annotations

import numpy as np


class WakeWordDetector:
    def __init__(self, wakeword: str, model_path: str = "") -> None:
        self.wakeword = wakeword.lower().strip()
        self.model_path = model_path
        self.model = None
        self._load_optional_model()

    def _load_optional_model(self) -> None:
        try:
            from openwakeword.model import Model

            kwargs = {}
            if self.model_path:
                kwargs["wakeword_models"] = [self.model_path]
            self.model = Model(**kwargs)
        except Exception:
            self.model = None

    def detected(self, audio_chunk: np.ndarray, fallback_text: str | None = None) -> bool:
        if self.model is not None:
            preds = self.model.predict(audio_chunk)
            scores = [float(v) for v in preds.values()]
            return bool(scores and max(scores) > 0.5)

        if fallback_text:
            return self.wakeword in fallback_text.lower()
        return False
