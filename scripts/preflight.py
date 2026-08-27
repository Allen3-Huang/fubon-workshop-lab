from __future__ import annotations

import importlib.util
import shutil
import sys


def status(ok: bool, message: str) -> None:
    marker = "OK" if ok else "ACTION REQUIRED"
    print(f"[{marker}] {message}")


def main() -> int:
    python_ok = sys.version_info >= (3, 10)
    status(python_ok, f"Python {sys.version.split()[0]} (3.10+ required)")

    required_modules = ["fastapi", "httpx", "pytest", "ruff", "uvicorn"]
    missing = [
        module for module in required_modules if importlib.util.find_spec(module) is None
    ]
    status(
        not missing,
        "Python dependencies installed"
        if not missing
        else f"Run `uv sync` to install: {', '.join(missing)}",
    )

    uv_ok = shutil.which("uv") is not None
    status(uv_ok, "uv is available (install: https://docs.astral.sh/uv/)")

    status(shutil.which("git") is not None, "Git is available")
    status(
        shutil.which("gh") is not None,
        "GitHub CLI is available (optional; GitHub web UI can be used instead)",
    )
    return 0 if python_ok and uv_ok and not missing and shutil.which("git") else 1


if __name__ == "__main__":
    raise SystemExit(main())

