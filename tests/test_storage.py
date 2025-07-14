# tests/test_storage.py
from storage import (
    load_tasks_from_storage,
    add_task_to_storage,
    remove_task_from_storage,
    update_task_in_storage,
    finish_task_in_storage,
    undo_last_action_storage,
)
from datetime import date


def make_task(id="t1", name="foo", completed=False, due=None):
    return {
        "id": id,
        "name": name,
        "description": "",
        "created_at": "2025-07-14T00:00:00",
        "completed": completed,
        "due": due.isoformat() if isinstance(due, date) else due,
    }


def test_add_and_load_tasks(isolated_config_env):
    # storage starts empty
    assert load_tasks_from_storage() == []

    t = make_task(id="1", name="first")
    add_task_to_storage(t)
    tasks = load_tasks_from_storage()
    assert len(tasks) == 1
    assert tasks[0]["id"] == "1"
    assert tasks[0]["name"] == "first"


def test_remove_task_and_undo(isolated_config_env):
    t1 = make_task(id="1", name="one")
    t2 = make_task(id="2", name="two")
    add_task_to_storage(t1)
    add_task_to_storage(t2)

    # remove t1
    removed = remove_task_from_storage("1")
    assert removed["id"] == "1"
    tasks = load_tasks_from_storage()
    assert [t["id"] for t in tasks] == ["2"]

    # undo removal
    info = undo_last_action_storage()
    assert "Undid removal" in info["info"]
    tasks = load_tasks_from_storage()
    assert set(t["id"] for t in tasks) == {"1", "2"}


def test_update_task_and_undo(isolated_config_env):
    t = make_task(id="42", name="orig")
    add_task_to_storage(t)

    updated = update_task_in_storage("42", {"name": "changed", "due": "2025-12-31"})
    assert updated["name"] == "changed"
    assert updated["due"] == "2025-12-31"

    # undo update
    info = undo_last_action_storage()
    assert "Undid update" in info["info"]
    tasks = load_tasks_from_storage()
    assert tasks[0]["name"] == "orig"
    assert tasks[0].get("due") is None


def test_finish_task_and_undo(isolated_config_env):
    t = make_task(id="99", name="finish_me")
    add_task_to_storage(t)

    finished = finish_task_in_storage("99")
    assert finished["completed"] is True

    # undo finish
    info = undo_last_action_storage()
    assert "Undid finish" in info["info"]
    tasks = load_tasks_from_storage()
    assert tasks[0]["completed"] is False


def test_undo_add(isolated_config_env):
    t = make_task(id="ax", name="temporary")
    add_task_to_storage(t)

    # undo the add itself
    info = undo_last_action_storage()
    assert "Undid add" in info["info"]
    assert load_tasks_from_storage() == []
