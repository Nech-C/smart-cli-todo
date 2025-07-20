"""LangChain tools for interacting with the todo app."""

from typing import Optional
from langchain_core.tools import tool

from src.core import (
    add_task,
    finish_task,
    list_tasks,
    remove_task,
    update_task,
)
from src.utils import parse_date


@tool
def add_task_tool(name: str, description: str = "", due: str = "") -> dict:
    """Add a new task."""

    task = {"name": name, "description": description, "due": parse_date(due)}
    return add_task(task)


@tool
def list_tasks_tool(status: str = "all") -> list:
    """List tasks filtered by status."""

    tasks = list_tasks(status)
    return tasks


@tool
def update_task_tool(task_id: str, name: Optional[str] = None,
                     description: Optional[str] = None,
                     due: Optional[str] = None) -> dict:
    """Update an existing task."""

    fields = {
        "name": name,
        "description": description,
        "due": parse_date(due) if due else None,
    }
    return update_task(task_id, fields)


@tool
def finish_task_tool(task_id: str) -> dict:
    """Mark a task as finished."""

    return finish_task(task_id)


@tool
def remove_task_tool(task_id: str) -> dict:
    """Remove a task by id."""

    return remove_task(task_id)


@tool
def delete_task_tool(task_id: str) -> dict:
    """Alias for :func:`remove_task_tool`."""

    return remove_task(task_id)
