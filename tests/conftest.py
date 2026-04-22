import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

JARVIS_SRC = ROOT / "jarvis"
if str(JARVIS_SRC) not in sys.path:
    sys.path.insert(0, str(JARVIS_SRC))
