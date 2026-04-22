# Jarvis (Windows) — Local + Hybrid

Bu proje, Windows açılışında otomatik başlayan bir sesli asistan iskeleti sunar.

## Modlar
- `local`: Wake-word + Whisper + Ollama + Piper (tamamen yerel)
- `hybrid`: Wake-word + Whisper + OpenAI + Piper

## Özellikler
- `openWakeWord` ile tetikleme (opsiyonel)
- `faster-whisper` ile Türkçe STT
- Ollama veya OpenAI backend seçimi
- Piper ile yerel TTS
- Beyaz liste tabanlı komut çalıştırma
- MCP stdio server entegrasyonu (listeleme + tool çağırma)

## Kurulum
```powershell
cd C:\jarvis
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Çalıştırma
```powershell
python -m jarvis.main --mode local
python -m jarvis.main --mode hybrid
```

## Windows başlangıç
Görev Zamanlayıcı:
- Trigger: At log on
- Action: `C:\jarvis\.venv\Scripts\python.exe -m jarvis.main --mode local`

## MCP server örneği
`mcp_servers.json` içine server komutları eklenir:
```json
[
  {
    "name": "filesystem",
    "command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\Public"]
  }
]
```

> Not: MCP server süreçleri yerelde kurulu olmalıdır.
