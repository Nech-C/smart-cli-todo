import typer
from typing import List, Optional
from utils import parse_task_parts
from core import (
    add_task,
    list_tasks,
    update_task,
    finish_task,
    undo_last_action,
    search_task,
    init_todo,
    remove_task,
)

app = typer.Typer()


@app.command()
def add(task_parts: List[str]):
    """
    llm-todo add pay rent /d2000 dollars /2025-07-15 /repeat
    """
    task = parse_task_parts(task_parts)
    result = add_task(task)
    typer.echo(result["info"])


@app.command()
def list(
    which: Optional[str] = typer.Argument(
        "", help="Which tasks to show:  (none)= 'ongoing', 'done', or 'all'"
    ),
):
    """
    llm-todo list           # show pending
    llm-todo list done      # show only completed
    llm-todo list all       # show everything
    """
    # pick the right slice
    which = which.lower()
    if which == "":
        tasks = list_tasks(status="ongoing")
    elif which == "done":
        tasks = list_tasks(status="done")
    elif which == "all":
        tasks = list_tasks(status="all")
    elif which == "ongoing":
        tasks = list_tasks(status="ongoing")
    else:
        typer.echo("❗️ Invalid argument. Use `ongoing`, `done` or `all`.")
        raise typer.Exit(1)

    if not tasks:
        typer.echo("No tasks.")
        raise typer.Exit()

    # display with simple 1-based index
    for t in tasks:
        status = "✅" if t["completed"] else "❌"
        due = t.get("due") or ""
        typer.echo(f"{status} {t['name']} (due: {due})")


@app.command()
def finish():
    """
    finish an ongoing task. It prompts the user to select the task
    """
    tasks = list_tasks("ongoing")
    tasks.sort(key=lambda x: x["created_at"])
    for idx, task in enumerate(tasks, start=1):
        task["number"] = idx
        typer.echo(f"❌ {idx}. {task['name']} due: {task['due']}")
    while True:
        choices = input(
            "Type in the id(s) of tasks you have finished(separated by commas):"
        )
        choices = choices.split(",")
        try:
            choices = [int(choice.strip()) for choice in choices]
        except ValueError:
            print("Incorrect input format! try 1 or 1, 2, 3!")

        if min(choices) < 1 or max(choices) > len(tasks):
            print("ids out of bounds!")
        else:
            break

    for task in tasks:
        if task["number"] in choices:
            result = finish_task(task["id"])
            print(result["info"])


@app.command()
def remove(
    which: Optional[str] = typer.Argument(
        "ongoing", help="Which tasks to show:  (none)= 'ongoing', 'done', or 'all'"
    ),
):
    which = which.lower()
    if which not in ["ongoing", "done", "all"]:
        typer.echo("❗️ Invalid argument. Use `ongoing`, `done` or `all`.")
        raise typer.Exit(1)

    tasks = list_tasks(which)
    tasks.sort(key=lambda x: x["created_at"])
    for idx, task in enumerate(tasks, start=1):
        task["number"] = idx
        symbol = "❌" if task["status"] == "ongoing" else "✅"
        typer.echo(f"{symbol} {idx}. {task['name']} due: {task['due']}")
    while True:
        choices = input(
            "Type in the id(s) of tasks you want to remove(separated by commas):"
        )
        choices = choices.split(",")
        try:
            choices = [int(choice.strip()) for choice in choices]
        except ValueError:
            print("Incorrect input format! try something like 1 or 1, 2, 3!")

        if min(choices) < 1 or max(choices) > len(tasks):
            print("ids out of bounds!")
        else:
            break

    for task in tasks:
        if task["number"] in choices:
            result = remove_task(task["id"])
            print(result["info"])


@app.command()
def update(task_parts: List[str]):
    """
    llm-todo update 3 new name /d new desc /2025-08-01
    """
    if len(task_parts) < 2:
        typer.echo("Usage: llm-todo update <task#> <fields...>")
        raise typer.Exit(1)

    # pick your task
    idx = int(task_parts[0]) - 1
    all_tasks = list_tasks(include_completed=True)
    try:
        task_id = all_tasks[idx]["id"]
    except IndexError:
        typer.echo("Invalid task number.")
        raise typer.Exit(1)

    fields = parse_task_parts(task_parts[1:])
    result = update_task(task_id, fields)
    typer.echo(result["info"])


@app.command()
def undo():
    """
    Undo your last add/remove/update/finish.
    """
    result = undo_last_action()
    typer.echo(result["info"])


@app.command()
def search(query):
    # TODO: return ids
    tasks = search_task(query)
    for task in tasks:
        typer.echo(task)


@app.command()
def chat(prompt: str):
    # response = agent.run(prompt)
    # typer.echo(response)
    pass


@app.command()
def init():
    init_todo()


if __name__ == "__main__":
    app()
