from __future__ import annotations


class GoodMoodEngine:
    def __init__(self, boost: float = 1.2) -> None:
        self.mood_score = 50.0
        self.boost = boost

    def on_user_message(self, text: str) -> float:
        length_factor = min(len(text) / 120, 1.0)
        politeness_bonus = 5.0 if any(k in text.lower() for k in ["lütfen", "teşekkür", "thanks"]) else 0.0
        self.mood_score = min(100.0, self.mood_score + (2 + 10 * length_factor + politeness_bonus) * self.boost)
        return self.mood_score

    def on_error(self) -> float:
        self.mood_score = max(0.0, self.mood_score - 8)
        return self.mood_score

    def ironman_prefix(self) -> str:
        if self.mood_score >= 85:
            return "[IRONMAN-HUD: MAX POWER]"
        if self.mood_score >= 65:
            return "[IRONMAN-HUD: STABLE ARC]"
        return "[IRONMAN-HUD: RECOVERY]"
