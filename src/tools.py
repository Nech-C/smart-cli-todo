from langchain_core.tools import tool

from src.core import add_task, list_tasks
from src.utils import parse_date


@tool
def add_task_tool(name: str, description: str = "", due: str = "") -> dict:
    task = {"name": name, "description": description, "due_date": parse_date(due)}
    return add_task(task)["info"]


@tool
def list_tasks_tool(status: str):
    tasks = list_tasks(status)

    return tasks
