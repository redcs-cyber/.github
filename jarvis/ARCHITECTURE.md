# Jarvis Architecture — Ironman Grade

## Runtime Katmanları
1. **Input Layer**: Mic + STT + Wake Word
2. **Mood Layer**: GOODMOOD scoring
3. **Decision Layer**: CommandRouter + MCP gate
4. **Brain Layer**: MultiProviderRouter (Ollama -> DeepSeek -> OpenAI)
5. **Output Layer**: Piper TTS + optional OpenAL FX
6. **Observability**: Telemetry JSONL + Rich Live Ops

## Sequence
```mermaid
sequenceDiagram
  participant U as User
  participant S as STT
  participant W as Wake
  participant G as GoodMood
  participant R as Router
  participant B as MultiProvider
  participant T as TTS
  participant O as Telemetry

  U->>S: Voice
  S->>W: transcription
  W->>G: wake success
  G-->>O: mood_score
  S->>R: user prompt

  alt local command
    R->>T: result
    R-->>O: command.executed
  else llm request
    R->>B: prompt
    B-->>B: ollama/deepseek/openai fallback
    B->>T: reply
    B-->>O: llm.reply(provider,mood)
  end
```

## Data Contracts
Telemetry JSONL satırı:
```json
{
  "ts": 1713780000.12,
  "level": "info",
  "event": "llm.reply",
  "payload": {
    "provider": "deepseek",
    "mood_score": 87.4,
    "chars": 142
  }
}
```
