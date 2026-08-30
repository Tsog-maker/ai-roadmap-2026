"""log.md файлыг уншиж, бүтэцтэй өгөгдөл болгох."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date

DATE_HEADING = re.compile(r"^##\s+(\d{4})-(\d{2})-(\d{2})\s*$")


def parse_date_heading(line: str) -> date | None:
    """'## 2026-08-30' мөрөөс огноог гаргана. Огноо биш бол None."""
    match = DATE_HEADING.match(line.strip())
    if match is None:
        return None
    year, month, day = (int(part) for part in match.groups())
    try:
        return date(year, month, day)
    except ValueError:
        return None


FIELD_LINE = re.compile(r"^-\s*(?P<label>[^:]+):\s*(?P<value>.*)$")

LABELS = {
    "хийсэн": "done",
    "ойлгоогүй": "unclear",
    "маргааш": "tomorrow",
}


@dataclass
class Entry:
    """Нэг өдрийн бичлэг."""

    day: date
    done: list[str] = field(default_factory=list)
    unclear: list[str] = field(default_factory=list)
    tomorrow: list[str] = field(default_factory=list)


def parse_log(text: str) -> list[Entry]:
    """log.md-ийн бүх агуулгыг Entry жагсаалт болгоно."""
    entries: list[Entry] = []
    current: Entry | None = None

    for line in text.splitlines():
        day = parse_date_heading(line)
        if day is not None:
            current = Entry(day=day)
            entries.append(current)
            continue

        if current is None:
            continue

        match = FIELD_LINE.match(line.strip())
        if match is None:
            continue

        key = LABELS.get(match.group("label").strip().lower())
        if key is None:
            continue

        value = match.group("value").strip()
        if value:
            getattr(current, key).append(value)

    return entries
