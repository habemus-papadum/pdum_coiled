"""Utility helpers for locating built widget assets."""

from __future__ import annotations

from pathlib import Path

_WIDGETS_DIR = Path(__file__).parent


def get_widget_path() -> Path:
    """Return the path that contains the compiled widget bundle."""

    return _WIDGETS_DIR


def get_widget_js() -> str:
    """Return the compiled widget JavaScript bundle as a string."""

    js_path = _WIDGETS_DIR / "index.js"
    if not js_path.exists():
        raise FileNotFoundError(
            "Widget bundle not found. "
            "Run 'pnpm --filter @habemus-papadum/coiled-widgets build:python' before rendering widgets."
        )
    return js_path.read_text(encoding="utf-8")
