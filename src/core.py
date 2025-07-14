from uuid import uuid4
from datetime import datetime
from storage import (
    add_task_to_storage,
    load_tasks_from_storage,
    remove_task_from_storage,
    update_task_in_storage,
    finish_task_in_storage,
    undo_last_action_storage,
)


def add_task(task: dict) -> dict:
    task["id"] = str(uuid4())
    task["created_at"] = datetime.utcnow().isoformat()
    task["completed"] = False
    t = add_task_to_storage(task)
    return {"info": f"Added task '{t['name']}'", "task": t}


def list_tasks(include_completed: bool = False) -> list:
    tasks = load_tasks_from_storage()
    tasks.sort(key=lambda t: t["created_at"])
    if not include_completed:
        tasks = [t for t in tasks if not t["completed"]]
    return tasks


def update_task(task_id: str, fields: dict) -> dict:
    t = update_task_in_storage(task_id, fields)
    return {"info": f"Updated task '{t['name']}'", "task": t}


def finish_task(task_id: str) -> dict:
    t = finish_task_in_storage(task_id)
    return {"info": f"Finished task '{t['name']}'", "task": t}


def remove_task(task_id: str) -> dict:
    t = remove_task_from_storage(task_id)
    return {"info": f"Removed task '{t['name']}'", "task": t}


def undo_last_action() -> dict:
    return undo_last_action_storage()
