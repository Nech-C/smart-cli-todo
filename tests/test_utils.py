from datetime import date, timedelta

from utils import parse_date, parse_task_parts


def test_parse_date_basic():
    today = date.today()
    assert parse_date("today") == today
    assert parse_date("tomorrow") == today + timedelta(days=1)
    assert parse_date("2025-01-02") == date(2025, 1, 2)
    assert parse_date("bad-date") is None


def test_parse_task_parts_full():
    parts = ["pay", "rent", "/d2000", "dollars", "/2030-05-01", "/repeat"]
    task = parse_task_parts(parts)
    assert task["name"] == "pay rent"
    assert task["description"] == "2000 dollars"
    assert task["due"] == date(2030, 5, 1)
    assert task["repeat"] is True


def test_parse_task_parts_invalid_date(capsys):
    task = parse_task_parts(["task", "/bad"])
    captured = capsys.readouterr()
    assert "Failed to parse" in captured.out
    assert task["due"] is None
