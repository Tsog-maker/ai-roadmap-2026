from datetime import date

import pytest

from ai_roadmap_2026.logsum import parse_date_heading, parse_log

SAMPLE = """# Learning Log

## 2026-08-30

- Хийсэн: uv суулгав
- Ойлгоогүй: venv гэж юу вэ
- Маргааш: Colab шалгах

## 2026-08-31

- Хийсэн: type hints
- Санамж: энэ шошгыг мэдэхгүй
- Ойлгоогүй: regex-ийн нэртэй бүлэг
"""


@pytest.mark.parametrize(
    ("line", "expected"),
    [
        ("## 2026-08-30", date(2026, 8, 30)),
        ("  ## 2026-01-01  ", date(2026, 1, 1)),
        ("# Learning Log", None),
        ("- Хийсэн: юм", None),
        ("", None),
        ("## 2026-8-30", None),
        ("## 2026-13-01", None),
    ],
)
def test_parse_date_heading(line: str, expected: date | None) -> None:
    assert parse_date_heading(line) == expected


def test_parse_log_finds_all_days() -> None:
    entries = parse_log(SAMPLE)
    assert len(entries) == 2
    assert entries[0].day == date(2026, 8, 30)
    assert entries[1].day == date(2026, 8, 31)


def test_parse_log_collects_fields() -> None:
    first = parse_log(SAMPLE)[0]
    assert first.done == ["uv суулгав"]
    assert first.unclear == ["venv гэж юу вэ"]
    assert first.tomorrow == ["Colab шалгах"]


def test_parse_log_ignores_unknown_labels() -> None:
    second = parse_log(SAMPLE)[1]
    assert second.done == ["type hints"]
    assert second.unclear == ["regex-ийн нэртэй бүлэг"]
    assert second.tomorrow == []


def test_parse_log_empty_text() -> None:
    assert parse_log("") == []
