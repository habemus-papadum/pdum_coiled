"""Rendering helpers for coiled widgets."""

from __future__ import annotations

import html
import json
from textwrap import dedent
from typing import Any

from .utils import get_widget_js
from .widget import Widget

_DATA_ATTRIBUTE = "data-coiled-widget"


def js_prelude() -> str:
    """Return the script tag that bootstraps the widget bundle."""

    bundle = get_widget_js()
    return f"<script>\n{bundle}\n</script>"


def setup_notebook() -> None:
    """Inject the widget bundle into an interactive environment like Jupyter."""

    try:
        from IPython.display import HTML, display  # type: ignore
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "IPython is required to setup notebook widgets. Install it or run outside notebooks."
        ) from exc

    display(HTML(js_prelude()))


def _normalize_payload(widget: Widget | dict[str, Any]) -> dict[str, Any]:
    if isinstance(widget, Widget):
        return widget.to_payload()
    return widget


def render_widget_html(widget: Widget | dict[str, Any]) -> str:
    """Return an HTML snippet that renders a widget when the bundle is loaded."""

    payload = _normalize_payload(widget)
    encoded = html.escape(json.dumps(payload))
    return dedent(
        f"""
        <div class="tp-widget-host" {_DATA_ATTRIBUTE}="{encoded}"></div>
        """
    ).strip()
