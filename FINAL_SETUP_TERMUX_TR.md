# Jarvis 10x — Termux Kurulum Rehberi

Android + Termux üzerinde Jarvis API/dashboard + core runtime çalıştırmak için hızlı rehber.

## 1) Termux kur
- F-Droid üzerinden güncel Termux önerilir.

## 2) Depoyu klonla
```bash
pkg update -y && pkg upgrade -y
pkg install -y git

git clone <REPO_URL>
cd .github
```

## 3) Otomatik kurulum
```bash
bash scripts/install_termux.sh
```

## 4) Ortam dosyalarını hazırla
```bash
cp jarvis/.env.example jarvis/.env
cp jarvis/mcp_servers.example.json jarvis/mcp_servers.json
```

## 5) Self-check
```bash
source .venv/bin/activate
python tools/self_check.py
```

## 6) Çalıştır
```bash
bash scripts/run_termux.sh
```

## 7) Yerel erişim
- Dashboard: `http://127.0.0.1:8000/dashboard`
- Metrics: `http://127.0.0.1:8000/metrics`
- Status: `http://127.0.0.1:8000/status`

## 8) Notlar
- Termux'ta mikrofon/ses tarafı (pyaudio/openal) cihaz ve izinlere göre kısıtlı olabilir.
- Bu durumda API + dashboard + text akışı normal çalışır, sesli mod için ek ayar gerekebilir.
