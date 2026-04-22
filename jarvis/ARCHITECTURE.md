# Jarvis Architecture — Ultimate Professional Stack

## Runtime Katmanları
1. **Input Layer**: Mic + STT + Wake Word
2. **Agent Layer**: PlannerAgent + SafetyAgent + PersonaAgent
3. **Decision Layer**: CommandRouter + MCP gate
4. **Brain Layer**: MultiProviderRouter (Ollama -> DeepSeek -> OpenAI)
5. **Output Layer**: Piper TTS + optional OpenAL FX
6. **Observability**: Telemetry JSONL + FastAPI `/metrics` + Web Dashboard `/dashboard`

## Sequence
```mermaid
sequenceDiagram
  participant U as User
  participant S as STT
  participant A as AgentOrchestrator
  participant R as Router
  participant B as MultiProvider
  participant T as TTS
  participant O as Telemetry
  participant D as Dashboard

  U->>S: Voice
  S->>A: user text
  A-->>A: plan + safety + persona
  A-->>O: risk_level
  S->>R: parsed command

  alt local command
    R->>T: result
    R-->>O: command.executed
  else llm request
    R->>B: planned prompt
    B-->>B: provider fallback
    B->>T: reply
    B-->>O: llm.reply(provider,risk,mood)
  end

  O->>D: /metrics stream
```

## Data Contract (LLM reply)
```json
{
  "event": "llm.reply",
  "payload": {
    "provider": "ollama",
    "risk_level": "low",
    "mood_score": 88.1,
    "chars": 164
  }
}
```
