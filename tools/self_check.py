from __future__ import annotations

import importlib
from pathlib import Path


REQUIRED_MODULES = [
    "fastapi",
    "uvicorn",
    "requests",
    "openai",
    "pytest",
]


def check_files() -> list[str]:
    required = [
        Path("run.py"),
        Path("api/server.py"),
        Path("api/static/dashboard.html"),
        Path("jarvis/.env.example"),
        Path(".github/workflows/build.yml"),
    ]
    missing = [str(p) for p in required if not p.exists()]
    return missing


def main() -> None:
    missing_modules = []
    for name in REQUIRED_MODULES:
        try:
            importlib.import_module(name)
        except Exception:
            missing_modules.append(name)

    missing_files = check_files()

    if missing_modules or missing_files:
        print("SELF CHECK FAILED")
        if missing_modules:
            print(f"missing_modules={missing_modules}")
        if missing_files:
            print(f"missing_files={missing_files}")
        raise SystemExit(1)

    print("SELF CHECK OK")


if __name__ == "__main__":
    main()
