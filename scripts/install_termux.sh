#!/data/data/com.termux/files/usr/bin/bash
set -euo pipefail

echo "[1/6] Paket listesi güncelleniyor..."
pkg update -y && pkg upgrade -y

echo "[2/6] Gerekli paketler kuruluyor..."
pkg install -y python git clang cmake make libffi openssl

echo "[3/6] Sanal ortam oluşturuluyor..."
python -m venv .venv
source .venv/bin/activate

echo "[4/6] Pip güncelleniyor..."
python -m pip install --upgrade pip wheel setuptools

echo "[5/6] Python paketleri kuruluyor..."
pip install -r requirements.txt

echo "[6/6] Testler çalıştırılıyor..."
pytest -q || true

echo "Kurulum tamamlandı. Çalıştırma:"
echo "source .venv/bin/activate && python run.py"
