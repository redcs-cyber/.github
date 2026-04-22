Param(
  [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
Write-Host "[1/5] Virtual environment oluşturuluyor..."
& $Python -m venv .venv

Write-Host "[2/5] venv aktif ediliyor..."
& .\.venv\Scripts\Activate.ps1

Write-Host "[3/5] Paketler kuruluyor..."
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r jarvis/requirements.txt

Write-Host "[4/5] Testler çalıştırılıyor..."
pytest -q

Write-Host "[5/5] Kurulum tamamlandı. Çalıştırma komutu:"
Write-Host ".\.venv\Scripts\python.exe run.py"
