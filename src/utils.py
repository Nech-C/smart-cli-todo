# src/utils.py
from datetime import date, timedelta, datetime
from typing import List, Optional


def parse_task_parts(parts: List[str]) -> dict:
    """Parse CLI parts into a task dict (name, description, due, repeat)."""
    name_parts, description_parts = [], []
    due = None
    repeat = False
    parsing_desc = False

    for part in parts:
        if part.startswith("/"):
            parsing_desc = False
            if part.startswith("/d"):
                parsing_desc = True
                text = part[2:]
                if text:
                    description_parts.append(text)
            elif part == "/repeat":
                repeat = True
            else:
                due = part[1:]
        else:
            if parsing_desc:
                description_parts.append(part)
            else:
                name_parts.append(part)

    due_date = None
    if due:
        due_date = parse_date(due)
        if not due_date:
            print(
                f"Failed to parse '{due}'! Please use 'today', 'tomorrow', or 'YYYY-MM-DD'"
            )
    return {
        "name": " ".join(name_parts),
        "description": " ".join(description_parts),
        "due": due_date,
        "repeat": repeat,
    }


def parse_date(date_str: str) -> Optional[date]:
    """Convert a string into a date object."""
    if date_str == "today":
        return date.today()
    if date_str == "tomorrow":
        return date.today() + timedelta(days=1)
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
