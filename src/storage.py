import json
from datetime import datetime, timezone
from copy import deepcopy
from config import get_task_path, get_history_path


def _read_history():
    p = get_history_path()
    try:
        data = p.read_text().strip()
        return json.loads(data) if data else None
    except FileNotFoundError:
        return None


def _write_history(record: dict):
    get_history_path().write_text(json.dumps(record, indent=2))


def _clear_history():
    get_history_path().unlink(missing_ok=True)


def load_tasks_from_storage() -> list:
    path = get_task_path()
    with open(path, "r") as f:
        wrapper = json.load(f)
    return wrapper.get("tasks", [])


def save_tasks_to_storage(tasks: list):
    path = get_task_path()
    with open(path, "w") as f:
        json.dump({"tasks": tasks}, f, indent=2)


def add_task_to_storage(task: dict) -> dict:
    tasks = load_tasks_from_storage()
    tasks.append(task)
    save_tasks_to_storage(tasks)
    _write_history({"action": "add", "task": task})
    return task


def remove_task_from_storage(task_id: str) -> dict:
    tasks = load_tasks_from_storage()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            removed = tasks.pop(i)
            save_tasks_to_storage(tasks)
            _write_history({"action": "remove", "task": removed})
            return removed
    raise KeyError(f"Task {task_id} not found")


def update_task_in_storage(task_id: str, fields: dict) -> dict:
    tasks = load_tasks_from_storage()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            before = deepcopy(t)
            # only update non‐None fields
            for k, v in fields.items():
                if v is not None:
                    t[k] = v
            t["updated_at"] = datetime.now(timezone.utc).isoformat()
            tasks[i] = t
            save_tasks_to_storage(tasks)
            _write_history({"action": "update", "before": before, "after": t})
            return t
    raise KeyError(f"Task {task_id} not found")


def finish_task_in_storage(task_id: str) -> dict:
    tasks = load_tasks_from_storage()
    for i, t in enumerate(tasks):
        if t["id"] == task_id:
            before = deepcopy(t)
            t["completed"] = True
            t["completed_at"] = datetime.now(timezone.utc).isoformat()
            tasks[i] = t
            save_tasks_to_storage(tasks)
            _write_history({"action": "finish", "before": before, "after": t})
            return t
    raise KeyError(f"Task {task_id} not found")


def undo_last_action_storage() -> dict:
    hist = _read_history()
    if not hist:
        return {"info": "Nothing to undo."}

    action = hist["action"]
    # invert each action
    if action == "add":
        # remove the just‐added
        tid = hist["task"]["id"]
        remove_task_from_storage(tid)
        info = f"Undid add of '{hist['task']['name']}'"
    elif action == "remove":
        tasks = load_tasks_from_storage()
        tasks.append(hist["task"])
        # keep chronological order:
        tasks.sort(key=lambda t: t["created_at"])
        save_tasks_to_storage(tasks)
        info = f"Undid removal of '{hist['task']['name']}'"
    elif action == "update":
        # revert to before
        b = hist["before"]
        remove_task_from_storage(hist["after"]["id"])
        # and re‐add the before snapshot
        add_task_to_storage(b)
        info = f"Undid update of '{b['name']}'"
    elif action == "finish":
        tid = hist["before"]["id"]
        # revert completed flag
        tasks = load_tasks_from_storage()
        for i, t in enumerate(tasks):
            if t["id"] == tid:
                tasks[i] = hist["before"]
                break
        save_tasks_to_storage(tasks)
        info = f"Undid finish of '{hist['before']['name']}'"
    else:
        info = "Unknown action in history."

    _clear_history()
    return {"info": info}
