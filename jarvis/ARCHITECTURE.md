# Jarvis Architecture & Data Contracts

## 1) Runtime Bileşenleri
- `main.py`: Orkestrasyon döngüsü
- `audio.py`: Mikrofon kayıt chunk'ları
- `stt.py`: Ses->metin
- `wakeword.py`: Tetik kelime doğrulama
- `commands.py`: Güvenli komut whitelist
- `backends/*`: LLM sağlayıcıları
- `tts.py`: Metin->ses
- `integrations/mcp_client.py`: MCP stdio bağlantısı
- `telemetry.py`: Event logging
- `ui_console.py`: Operasyon paneli

## 2) Sequence Diagram
```mermaid
sequenceDiagram
  participant U as User
  participant Mic as Microphone
  participant STT as WhisperSTT
  participant W as Wakeword
  participant R as CommandRouter
  participant B as LLM Backend
  participant T as PiperTTS
  participant M as MCP Client
  participant O as Telemetry

  U->>Mic: konuşma
  Mic->>STT: audio chunk
  STT->>W: transcribe + detect
  W-->>O: wake.detected

  alt whitelist komut
    STT->>R: kullanıcı isteği
    R-->>O: command.executed
    R->>T: result text
  else normal LLM
    STT->>B: prompt
    alt mcp anahtar kelimesi
      B->>M: tools/list or tools/call
      M-->>O: mcp.connected/mcp.error
    end
    B-->>O: llm.reply
    B->>T: reply text
  end

  T->>U: sesli yanıt
```

## 3) Telemetry JSONL Sözleşmesi
Her satır bağımsız bir JSON eventidir:

```json
{
  "ts": 1713780000.12,
  "level": "info",
  "event": "user.prompt",
  "payload": {
    "text": "jarvis not defteri aç"
  }
}
```

## 4) MCP Server Sözleşmesi
`mcp_servers.json`:
```json
[
  {
    "name": "filesystem",
    "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Public"]
  }
]
```

## 5) Deployment Profilleri
- **Edge/Offline**: Ollama + Piper + Whisper CPU
- **Hybrid**: OpenAI + Piper + Whisper
- **Debug/Visual**: `--visual` ile canlı panel + JSONL telemetri
