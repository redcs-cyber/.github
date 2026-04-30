from __future__ import annotations

import math
from array import array


class OpenALFx:
    """Optional OpenAL effect layer (fallback-safe)."""

    def __init__(self) -> None:
        self.enabled = False
        try:
            from openal import oalInit  # type: ignore

            oalInit()
            self.enabled = True
        except Exception:
            self.enabled = False

    def arc_reactor_ping(self) -> None:
        if not self.enabled:
            return
        try:
            from openal import AL_FORMAT_MONO16, oalGetListener, oalOpenBuffer  # type: ignore

            sr = 22050
            duration = 0.12
            freq = 880
            samples = int(sr * duration)
            data = array(
                "h", (int(16000 * math.sin(2 * math.pi * freq * i / sr)) for i in range(samples))
            )
            buf = oalOpenBuffer(data.tobytes(), AL_FORMAT_MONO16, sr)
            src = buf.play()
            listener = oalGetListener()
            listener.move_to((0, 0, 0))
            src.stop()
        except Exception:
            return
