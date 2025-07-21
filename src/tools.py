# src/tools.py
"""LangChain tools for interacting with the todo app."""

from __future__ import annotations

from datetime import date
from typing import Optional

from langchain_core.tools import tool

from src.core import (
    add_task,
    finish_task,
    list_tasks,
    remove_task,
    update_task,
    search_task,
)
from src.utils import parse_date


def _parse_due(due: str | None) -> date | None:
    """Parse human-style date strings or return None."""
    if not due:
        return None
    parsed = parse_date(due)
    if parsed is None:
        raise ValueError("Unrecognised date; try 'today', 'tomorrow' or YYYY-MM-DD.")
    return parsed


@tool(description="Add a new task to the list.")
def add_task_tool(
    name: str,
    description: str = "",
    due: Optional[str] = None,
) -> dict:
    """
    Examples
    --------
    >>> add_task_tool(
    ...   name="Pay rent",
    ...   description="Transfer via bank app",
    ...   due="2025-08-01"
    ... )
    """
    task = {"name": name, "description": description, "due": _parse_due(due)}
    return add_task(task)


@tool(description="List tasks. status ∈ {'all','ongoing','done'}.")
def list_tasks_tool(status: str = "all") -> list:
    return list_tasks(status)


@tool(description="Update a task’s fields by id.")
def update_task_tool(
    task_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    due: Optional[str] = None,
) -> dict:
    fields = {
        "name": name,
        "description": description,
        "due": _parse_due(due),
    }
    return update_task(task_id, fields)


@tool(description="Mark a task finished by id.")
def finish_task_tool(task_id: str) -> dict:
    return finish_task(task_id)


@tool(description="Remove a task by id.")
def remove_task_tool(task_id: str) -> dict:
    return remove_task(task_id)


@tool(description="Semantic search across tasks (vector store).")
def search_task_tool(query: str, k: int = 5) -> list:
    """
    Example: search_task_tool(query="rent", k=3)
    """
    return search_task(query, k)
