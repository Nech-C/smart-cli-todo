# src/core.py
from enum import Enum
from uuid import uuid4
from datetime import datetime, timezone

from storage import (
    add_task_to_storage,
    load_tasks_from_storage,
    remove_task_from_storage,
    update_task_in_storage,
    finish_task_in_storage,
    undo_last_action_storage,
)
from semantic import add_task_vector, search_task_vector, remove_task_vector
from config import init


class Status(Enum):
    ONGOING = "ongoing"
    DONE = "done"
    CANCELLED = "cancelled"


def add_task(task: dict) -> dict:
    task["id"] = str(uuid4())
    task["created_at"] = datetime.now(timezone.utc).isoformat()
    task["status"] = Status.ONGOING.value
    task["completed"] = False

    add_task_to_storage(task)

    task["text"] = task["name"] + task["description"]
    task["metadata"] = {"status": task["status"]}
    add_task_vector(task)

    return {"info": f"Added task '{task['name']}'", "task": task}


def list_tasks(include_completed: bool = False) -> list:
    tasks = load_tasks_from_storage()
    tasks.sort(key=lambda t: t["created_at"])
    if not include_completed:
        tasks = [t for t in tasks if t.get("status") != Status.DONE.value]
    return tasks


def update_task(task_id: str, fields: dict) -> dict:
    t = update_task_in_storage(task_id, fields)
    return {"info": f"Updated task '{t['name']}'", "task": t}


def finish_task(task_id: str) -> dict:
    t = finish_task_in_storage(task_id)
    return {"info": f"Finished task '{t['name']}'", "task": t}


def remove_task(task_id: str) -> dict:
    t = remove_task_from_storage(task_id)
    remove_task_vector(task_id)
    return {"info": f"Removed task '{t['name']}'", "task": t}


def undo_last_action() -> dict:
    return undo_last_action_storage()


def search_task(query: str, k: int = 5):
    results = search_task_vector(query, k)
    tasks, _ = zip(*results)
    return tasks


def init_todo():
    init()
