from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentDecision:
    system_prompt: str
    final_prompt: str
    risk_level: str


class PlannerAgent:
    def build_prompt(self, user_text: str) -> str:
        return f"Kullanıcı hedefi: {user_text}\nKısa, uygulanabilir, adım odaklı yanıt üret."


class SafetyAgent:
    BLOCKED = ["format", "rm -rf", "delete system32", "shutdown /s", "drop database"]

    def assess(self, text: str) -> str:
        lowered = text.lower()
        if any(k in lowered for k in self.BLOCKED):
            return "high"
        if any(k in lowered for k in ["admin", "registry", "powershell"]):
            return "medium"
        return "low"


class PersonaAgent:
    def system_prompt(self, ironman: bool) -> str:
        base = "Sen profesyonel masaüstü asistanısın. Güvenli, net ve kısa cevap ver."
        if ironman:
            return base + " Ton: Stark/JARVIS tarzı, teknik ama sade, motive edici."
        return base


class AgentOrchestrator:
    def __init__(self) -> None:
        self.planner = PlannerAgent()
        self.safety = SafetyAgent()
        self.persona = PersonaAgent()

    def prepare(self, user_text: str, ironman: bool) -> AgentDecision:
        risk = self.safety.assess(user_text)
        planned = self.planner.build_prompt(user_text)
        system = self.persona.system_prompt(ironman)

        if risk == "high":
            safe_prompt = "Bu istek yüksek riskli. Kullanıcıya güvenli alternatif öner."
            return AgentDecision(system_prompt=system, final_prompt=safe_prompt, risk_level=risk)

        if risk == "medium":
            planned += "\nNot: Yalnızca güvenli ve geri alınabilir adımlar öner."

        return AgentDecision(system_prompt=system, final_prompt=planned, risk_level=risk)
