from pathlib import Path

from api.telemetry_service import TelemetryService


def test_summarize_counts_events_and_providers(tmp_path: Path):
    telemetry_file = tmp_path / "events.jsonl"
    telemetry_file.write_text(
        "\n".join(
            [
                '{"event":"jarvis.started","payload":{}}',
                '{"event":"llm.reply","payload":{"provider":"ollama","risk_level":"low"}}',
                '{"event":"llm.reply","payload":{"provider":"deepseek","risk_level":"medium"}}',
            ]
        ),
        encoding="utf-8",
    )

    service = TelemetryService(telemetry_file)
    summary = service.summarize()

    assert summary["event_count"] == 3
    assert summary["providers"]["ollama"] == 1
    assert summary["providers"]["deepseek"] == 1
    assert summary["risk_levels"]["low"] == 1
    assert summary["risk_levels"]["medium"] == 1
