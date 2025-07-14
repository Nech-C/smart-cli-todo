# tests/test_core.py
from core import (
    add_task,
    list_tasks,
    update_task,
    finish_task,
    remove_task,
    undo_last_action,
)


def test_core_full_flow(isolated_config_env):
    # add a task
    result = add_task(
        {"name": "do stuff", "description": "", "due": None, "repeat": False}
    )
    assert "Added task" in result["info"]
    tid = result["task"]["id"]

    # list pending
    pending = list_tasks()
    assert len(pending) == 1
    assert pending[0]["id"] == tid

    # update name
    upd = update_task(tid, {"name": "do more stuff"})
    assert "Updated task" in upd["info"]
    all_tasks = list_tasks(include_completed=True)
    assert all_tasks[0]["name"] == "do more stuff"

    # finish it
    fin = finish_task(tid)
    assert "Finished task" in fin["info"]
    assert list_tasks() == []  # no pending
    assert list_tasks(include_completed=True)[0]["completed"]

    # undo finish
    u1 = undo_last_action()
    assert "Undid finish" in u1["info"]
    assert list_tasks()[0]["completed"] is False

    # remove it
    rm = remove_task(tid)
    assert "Removed task" in rm["info"]
    assert list_tasks(include_completed=True) == []

    # undo removal
    u2 = undo_last_action()
    assert "Undid removal" in u2["info"]
    restored = list_tasks()
    assert restored[0]["id"] == tid
