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
    """add a task to storage

    Args:
        task (dict): {

                    }

    Returns:
        dict: _description_
    """
    task["id"] = str(uuid4())
    task["created_at"] = datetime.now(timezone.utc).isoformat()
    task["status"] = Status.ONGOING.value
    task["completed"] = False
    task["text"] = task["name"] + task["description"]
    task["metadata"] = {"status": task["status"]}
    task["indexed"] = False

    add_task_to_storage(task)

    return {"info": f"Added task '{task['name']}'", "task": task}


def list_tasks(status: str = "all") -> list:
    """List all tasks with the specified status

    Args:
        status (str): The status has to be one of "all", "ongoing", or "done"

    Returns:
        list: The list of tasks
    """
    if status not in {"all", "ongoing", "done"}:
        print(f"Unknow status: {status}.")
        return
    tasks = load_tasks_from_storage()
    if status == "all":
        return tasks
    tasks = [task for task in tasks if task["status"] == status]
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


def _index_tasks():
    tasks = load_tasks_from_storage()
    unindexed_tasks = [task for task in tasks if not task["indexed"]]

    for task in unindexed_tasks:
        add_task_vector(task)


def search_task(query: str, k: int = 5):
    _index_tasks()
    results = search_task_vector(query, k)
    tasks, _ = zip(*results)
    return tasks


def init_todo():
    init()
