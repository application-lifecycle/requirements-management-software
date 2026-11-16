#!/usr/bin/env python3
"""Pre-render all tools from tools.json into docs/index.html for zero-JS SEO."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS_PATH = ROOT / "tools.json"
INDEX_PATH = ROOT / "docs" / "index.html"

START_MARKER = "<!-- PRERENDER:TOOLS_START -->"
END_MARKER = "<!-- PRERENDER:TOOLS_END -->"


def render_card(tool: dict) -> str:
    caps = tool["capabilities"]
    cap_items = [
        ("Traceability", caps["traceability_matrix"]),
        ("ReqIF", caps["reqif"]),
        ("Baselines", caps["baselines"]),
        ("Git", caps["git_integration"]),
        ("Test linking", caps["test_linking"]),
    ]
    cap_html = "".join(
        f'<span class="cap-tag {"cap-tag--yes" if yes else ""}">{html.escape(label)}: {"Yes" if yes else "No"}</span>'
        for label, yes in cap_items
    )
    compliance = ", ".join(tool.get("compliance", [])) or "General engineering"
    github_link = (
        f'<a href="{html.escape(tool["github"])}" target="_blank" rel="noopener">GitHub</a>'
        if tool.get("github")
        else ""
    )
    return (
        f'<article class="cut tool-card" data-id="{html.escape(tool["id"])}">'
        f'<div class="tool-card__top">'
        f'<h3 class="tool-card__name">{html.escape(tool["name"])}</h3>'
        f'<span class="tool-card__license">{html.escape(tool["license_name"])}</span>'
        f"</div>"
        f'<p class="tool-card__tagline">{html.escape(tool["tagline"])}</p>'
        f'<p class="tool-card__meta">Pricing: {html.escape(tool["pricing"])}</p>'
        f'<p class="tool-card__meta">Standards: {html.escape(compliance)}</p>'
        f'<div class="tool-card__caps">{cap_html}</div>'
        f'<div class="tool-card__foot">'
        f'<div class="tool-card__links">'
        f'<a href="{html.escape(tool["website"])}" target="_blank" rel="noopener">Official site</a>'
        f"{github_link}"
        f"</div>"
        f'<button type="button" class="key key--sm" data-compare="{html.escape(tool["id"])}">Compare</button>'
        f"</div>"
        f"</article>"
    )


def main() -> int:
    data = json.loads(TOOLS_PATH.read_text(encoding="utf-8"))
    cards = "\n          ".join(render_card(t) for t in data["tools"])
    content = INDEX_PATH.read_text(encoding="utf-8")
    if START_MARKER not in content or END_MARKER not in content:
        raise RuntimeError("Missing PRERENDER markers in docs/index.html")
    before, rest = content.split(START_MARKER, 1)
    _, after = rest.split(END_MARKER, 1)
    updated = f"{before}{START_MARKER}\n          {cards}\n          {END_MARKER}{after}"
    INDEX_PATH.write_text(updated, encoding="utf-8")
    print(f"Pre-rendered {len(data['tools'])} tools into {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
