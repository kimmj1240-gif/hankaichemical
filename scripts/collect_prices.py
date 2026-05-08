#!/usr/bin/env python3
"""Collect daily plastic resin prices and append to data/prices.csv.

Sources are pluggable. By default this uses a placeholder source that records
"N/A" rows so the daily commit history is preserved. Replace `fetch_*`
functions to integrate real data sources (KPIA, public scraping, paid API).
"""
from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
RESINS_PATH = ROOT / "data" / "resins.json"
PRICES_PATH = ROOT / "data" / "prices.csv"

KST = timezone(timedelta(hours=9))


@dataclass
class PriceRow:
    date: str
    category: str  # "virgin" | "recycled"
    code: str
    name: str
    grade: str
    price_krw_per_kg: str  # numeric string or "" when unavailable
    source: str
    note: str


def load_resins() -> dict:
    with RESINS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def fetch_virgin_prices(today: str) -> list[PriceRow]:
    """Hook for virgin resin prices. Returns empty values by default."""
    rows: list[PriceRow] = []
    resins = load_resins()
    for r in resins["virgin"]:
        rows.append(PriceRow(
            date=today,
            category="virgin",
            code=r["code"],
            name=r["name_ko"],
            grade=r["grade"],
            price_krw_per_kg="",
            source="manual",
            note="awaiting input",
        ))
    return rows


def fetch_recycled_prices(today: str) -> list[PriceRow]:
    """Hook for recycled resin prices. Returns empty values by default."""
    rows: list[PriceRow] = []
    resins = load_resins()
    for r in resins["recycled"]:
        rows.append(PriceRow(
            date=today,
            category="recycled",
            code=r["code"],
            name=r["name_ko"],
            grade=r["grade"],
            price_krw_per_kg="",
            source="manual",
            note="awaiting input",
        ))
    return rows


def append_rows(rows: Iterable[PriceRow]) -> int:
    PRICES_PATH.parent.mkdir(parents=True, exist_ok=True)
    write_header = not PRICES_PATH.exists() or PRICES_PATH.stat().st_size == 0
    count = 0
    with PRICES_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "date", "category", "code", "name", "grade",
            "price_krw_per_kg", "source", "note",
        ])
        if write_header:
            writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
            count += 1
    return count


def already_collected(date_str: str) -> bool:
    if not PRICES_PATH.exists():
        return False
    with PRICES_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("date") == date_str:
                return True
    return False


def main() -> int:
    today = datetime.now(KST).strftime("%Y-%m-%d")
    if already_collected(today) and not os.environ.get("FORCE"):
        print(f"[skip] {today} already has rows in {PRICES_PATH.name}")
        return 0
    rows = fetch_virgin_prices(today) + fetch_recycled_prices(today)
    written = append_rows(rows)
    print(f"[ok] appended {written} rows for {today}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
