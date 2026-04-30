from jarvis.agents import AgentOrchestrator


def test_high_risk_prompt_is_blocked():
    orchestrator = AgentOrchestrator()
    decision = orchestrator.prepare("format c: now", ironman=True)

    assert decision.risk_level == "high"
    assert "güvenli alternatif" in decision.final_prompt.lower()


def test_medium_risk_adds_warning_note():
    orchestrator = AgentOrchestrator()
    decision = orchestrator.prepare("powershell script çalıştır", ironman=False)

    assert decision.risk_level == "medium"
    assert "yalnızca güvenli" in decision.final_prompt.lower()
