#!/usr/bin/env python3
"""Build a static dashboard (index.html) from data/prices.csv.

Embeds the CSV as JSON so the page works on GitHub Pages without any backend.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRICES_PATH = ROOT / "data" / "prices.csv"
RESINS_PATH = ROOT / "data" / "resins.json"
INDEX_PATH = ROOT / "index.html"


def load_rows() -> list[dict]:
    if not PRICES_PATH.exists():
        return []
    with PRICES_PATH.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    rows = load_rows()
    resins = json.loads(RESINS_PATH.read_text(encoding="utf-8"))
    payload = {"rows": rows, "resins": resins}
    template = (ROOT / "scripts" / "dashboard_template.html").read_text(encoding="utf-8")
    html = template.replace(
        "/*__DATA__*/",
        json.dumps(payload, ensure_ascii=False),
    )
    INDEX_PATH.write_text(html, encoding="utf-8")
    print(f"[ok] wrote {INDEX_PATH} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
