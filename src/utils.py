from datetime import date, timedelta, datetime
from typing import List


def parse_task_parts(parts: List[str]) -> dict:
    name_parts = []
    description_parts = []
    due = None
    repeat = False
    parsing_desc = False

    for part in parts:
        if part.startswith("/"):
            parsing_desc = False
            if part.startswith("/d"):
                # Start of description
                parsing_desc = True
                desc_text = part[2:]  # remove /d
                if desc_text:
                    description_parts.append(desc_text)
            elif part == "/repeat":
                repeat = True
            else:  # has to be due time
                due = part[1:]
        else:
            if parsing_desc:
                description_parts.append(part)
            else:
                name_parts.append(part)
    if due:
        due_date = parse_date(due)
        if not due_date:
            print(
                f"Failed to parse {due}! Please use"
                " a correct format: today, tomorrow, or 11-11-1111"
            )
    return {
        "name": " ".join(name_parts),
        "description": " ".join(description_parts),
        "due": due_date,
        "repeat": repeat,
    }


def parse_date(date_str):
    if date_str == "today":
        return date.today()
    if date_str == "tomorrow":
        return date.today() + timedelta(days=1)
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None
