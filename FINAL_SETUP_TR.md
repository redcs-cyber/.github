# Jarvis 10x — Final Kurulum (Windows)

Bu doküman proje için son kurulum adımlarını içerir.

## 1) Gereksinimler
- Windows 10/11
- Python 3.11+
- (Opsiyonel) Ollama kurulu ve model indirilmiş (`ollama pull llama3.1:8b`)
- (Opsiyonel) DeepSeek/OpenAI API anahtarları

## 2) Repo klonla
```powershell
git clone <REPO_URL>
cd .github
```

## 3) Tek komut kurulum (önerilen)
```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_windows.ps1
```

## 4) Ortam dosyalarını hazırla
```powershell
copy jarvis\.env.example jarvis\.env
copy jarvis\mcp_servers.example.json jarvis\mcp_servers.json
```

## 5) Self-check
```powershell
.\.venv\Scripts\python.exe tools/self_check.py
```
Beklenen çıktı: `SELF CHECK OK`

## 6) Çalıştır
```powershell
.\.venv\Scripts\python.exe run.py
```

## 7) Açılacak URL'ler
- Dashboard: http://127.0.0.1:8000/dashboard
- Metrics JSON: http://127.0.0.1:8000/metrics
- Status: http://127.0.0.1:8000/status

## 8) EXE Build
```powershell
.\.venv\Scripts\activate
pyinstaller run.py --onefile --name Jarvis
```
Çıktı: `dist/Jarvis.exe`

## 9) GitHub Actions Artifact
Push sonrası: **Actions > build > Artifacts > Jarvis**

## 10) Sorun Giderme
- `ModuleNotFoundError`: `pip install -r requirements.txt`
- `dashboard boş`: `jarvis/telemetry/events.jsonl` oluştuğunu kontrol et
- `ollama timeout`: `OLLAMA_URL` ve model adını `.env` içinde doğrula
