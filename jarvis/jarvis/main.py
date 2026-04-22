from __future__ import annotations

import argparse

from jarvis.audio import record_chunk
from jarvis.audio_fx import OpenALFx
from jarvis.agents import AgentOrchestrator
from jarvis.backends.router import MultiProviderRouter
from jarvis.commands import CommandRouter
from jarvis.config import load_mcp_servers, load_settings
from jarvis.integrations.mcp_client import MCPServerSpec, StdioMCPClient
from jarvis.ironman import GoodMoodEngine
from jarvis.stt import WhisperSTT
from jarvis.telemetry import Telemetry
from jarvis.tts import PiperTTS
from jarvis.ui_console import JarvisConsoleUI
from jarvis.wakeword import WakeWordDetector

BASE_SYSTEM_PROMPT = (
    "Sen masaüstü asistanısın. Güvenli ol, kısa cevap ver. "
    "Tehlikeli sistem komutlarını asla çalıştırma."
)


def bootstrap_mcp_clients(settings, telemetry: Telemetry):
    clients = []
    for server in load_mcp_servers(settings.mcp_servers_file):
        spec = MCPServerSpec(name=server["name"], command=server["command"])
        try:
            c = StdioMCPClient(spec)
            c.initialize()
            clients.append(c)
            telemetry.emit("mcp.connected", {"name": spec.name})
            print(f"[MCP] bağlı: {spec.name}")
        except Exception as exc:
            telemetry.emit("mcp.error", {"name": spec.name, "error": str(exc)}, level="error")
            print(f"[MCP] bağlanamadı: {spec.name} -> {exc}")
    return clients


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["local", "hybrid"], default=None)
    parser.add_argument("--visual", action="store_true", help="Rich live console panel aç")
    parser.add_argument("--ironman", action="store_true", help="GOODMOOD Ironman persona modu")
    args = parser.parse_args()

    settings = load_settings()
    mode = args.mode or settings.mode
    telemetry = Telemetry(settings.telemetry_file)
    ui = JarvisConsoleUI()
    mood = GoodMoodEngine(settings.goodmood_boost)
    fx = OpenALFx()
    agents = AgentOrchestrator()

    backend = MultiProviderRouter(settings)
    stt = WhisperSTT(settings.whisper_model, settings.whisper_device, settings.whisper_compute_type)
    tts = PiperTTS(settings.piper_exe, settings.piper_model, settings.piper_output_wav)
    wake = WakeWordDetector(settings.wakeword, settings.wakeword_model_path)
    router = CommandRouter()
    mcp_clients = bootstrap_mcp_clients(settings, telemetry)

    ui.set(status="running", mode=mode, wakeword=settings.wakeword, mcp_servers=len(mcp_clients))
    telemetry.emit("jarvis.started", {"mode": mode, "wakeword": settings.wakeword, "ironman": args.ironman})

    print(f"Jarvis başladı. Mod={mode}. Wake word='{settings.wakeword}'")
    tts.speak("Jarvis hazır.")

    live_ctx = ui.run_live() if args.visual else None

    try:
        if live_ctx:
            live_ctx.__enter__()
            live_ctx.update(ui.render())

        while True:
            audio = record_chunk(settings.sample_rate, settings.chunk_seconds)
            heard = stt.transcribe(audio, settings.sample_rate)
            if not heard:
                continue

            ui.set(last_heard=heard)
            telemetry.emit("audio.heard", {"text": heard})
            if live_ctx:
                live_ctx.update(ui.render())

            if not wake.detected(audio, fallback_text=heard):
                continue

            print(f"[wake] {heard}")
            fx.arc_reactor_ping()
            telemetry.emit("wake.detected", {"text": heard})
            tts.speak("Dinliyorum.")

            cmd_audio = record_chunk(settings.sample_rate, settings.chunk_seconds + 2)
            user_text = stt.transcribe(cmd_audio, settings.sample_rate)
            if not user_text:
                tts.speak("Sizi duyamadım.")
                telemetry.emit("user.missed")
                continue

            print(f"[user] {user_text}")
            mood_score = mood.on_user_message(user_text)
            ui.set(last_user=user_text)
            telemetry.emit("user.prompt", {"text": user_text, "mood_score": mood_score})
            if live_ctx:
                live_ctx.update(ui.render())

            local_result = router.handle(user_text)
            if local_result:
                print(f"[cmd] {local_result}")
                ui.set(last_reply=local_result)
                telemetry.emit("command.executed", {"result": local_result, "mood_score": mood_score})
                tts.speak(local_result)
                if live_ctx:
                    live_ctx.update(ui.render())
                continue

            try:
                if "mcp" in user_text.lower() and mcp_clients:
                    tools = mcp_clients[0].list_tools()
                    reply = f"MCP araçları hazır. {tools}"
                    telemetry.emit("mcp.tools_listed", {"count": len(tools) if isinstance(tools, list) else 1})
                else:
                    decision = agents.prepare(user_text, args.ironman)
                    result = backend.reply(decision.final_prompt, decision.system_prompt)
                    prefix = f"{mood.ironman_prefix()} " if args.ironman else ""
                    reply = f"{prefix}{result.content}"
                    telemetry.emit(
                        "llm.reply",
                        {
                            "chars": len(reply),
                            "provider": result.provider,
                            "mood_score": mood_score,
                            "risk_level": decision.risk_level,
                        },
                    )
            except Exception as exc:
                mood_after_error = mood.on_error()
                reply = "Sistem geçici olarak zorlanıyor; yeniden deniyorum komutan."
                telemetry.emit("llm.error", {"error": str(exc), "mood_score": mood_after_error}, level="error")

            print(f"[jarvis] {reply}")
            ui.set(last_reply=reply)
            if live_ctx:
                live_ctx.update(ui.render())
            tts.speak(reply)

    except KeyboardInterrupt:
        telemetry.emit("jarvis.stopped")
        print("Kapatılıyor...")
    finally:
        if live_ctx:
            live_ctx.__exit__(None, None, None)
        for c in mcp_clients:
            c.close()


if __name__ == "__main__":
    main()
