from __future__ import annotations

import argparse

from jarvis.audio import record_chunk
from jarvis.backends.ollama_backend import OllamaBackend
from jarvis.backends.openai_backend import OpenAIBackend
from jarvis.commands import CommandRouter
from jarvis.config import load_mcp_servers, load_settings
from jarvis.integrations.mcp_client import MCPServerSpec, StdioMCPClient
from jarvis.stt import WhisperSTT
from jarvis.tts import PiperTTS
from jarvis.wakeword import WakeWordDetector


SYSTEM_PROMPT = (
    "Sen masaüstü asistanısın. Güvenli ol, kısa cevap ver. "
    "Tehlikeli sistem komutlarını asla çalıştırma."
)


def build_backend(mode: str, settings):
    if mode == "hybrid":
        if not settings.openai_api_key:
            raise RuntimeError("Hybrid mod için OPENAI_API_KEY gerekli.")
        return OpenAIBackend(settings.openai_api_key, settings.openai_model)
    return OllamaBackend(settings.ollama_url, settings.ollama_model)


def bootstrap_mcp_clients(settings):
    clients = []
    for server in load_mcp_servers(settings.mcp_servers_file):
        spec = MCPServerSpec(name=server["name"], command=server["command"])
        try:
            c = StdioMCPClient(spec)
            c.initialize()
            clients.append(c)
            print(f"[MCP] bağlı: {spec.name}")
        except Exception as exc:
            print(f"[MCP] bağlanamadı: {spec.name} -> {exc}")
    return clients


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["local", "hybrid"], default=None)
    args = parser.parse_args()

    settings = load_settings()
    mode = args.mode or settings.mode

    backend = build_backend(mode, settings)
    stt = WhisperSTT(settings.whisper_model, settings.whisper_device, settings.whisper_compute_type)
    tts = PiperTTS(settings.piper_exe, settings.piper_model, settings.piper_output_wav)
    wake = WakeWordDetector(settings.wakeword, settings.wakeword_model_path)
    router = CommandRouter()
    mcp_clients = bootstrap_mcp_clients(settings)

    print(f"Jarvis başladı. Mod={mode}. Wake word='{settings.wakeword}'")
    tts.speak("Jarvis hazır.")

    try:
        while True:
            audio = record_chunk(settings.sample_rate, settings.chunk_seconds)
            heard = stt.transcribe(audio, settings.sample_rate)
            if not heard:
                continue

            if not wake.detected(audio, fallback_text=heard):
                continue

            print(f"[wake] {heard}")
            tts.speak("Dinliyorum.")

            cmd_audio = record_chunk(settings.sample_rate, settings.chunk_seconds + 2)
            user_text = stt.transcribe(cmd_audio, settings.sample_rate)
            if not user_text:
                tts.speak("Sizi duyamadım.")
                continue

            print(f"[user] {user_text}")

            local_result = router.handle(user_text)
            if local_result:
                print(f"[cmd] {local_result}")
                tts.speak(local_result)
                continue

            if "mcp" in user_text.lower() and mcp_clients:
                tools = mcp_clients[0].list_tools()
                reply = f"MCP araçları hazır. {tools}"
            else:
                reply = backend.reply(user_text, SYSTEM_PROMPT)

            print(f"[jarvis] {reply}")
            tts.speak(reply)

    except KeyboardInterrupt:
        print("Kapatılıyor...")
    finally:
        for c in mcp_clients:
            c.close()


if __name__ == "__main__":
    main()
