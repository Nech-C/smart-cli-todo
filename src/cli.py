import typer
from typing import List, Optional
from utils import parse_task_parts
from core import (
    add_task,
    list_tasks,
    update_task,
    finish_task,
    remove_task,
    undo_last_action,
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


@app.command(name="list")
def _list(
    which: Optional[str] = typer.Argument(
        None, help="Which tasks to show:  (none)=pending, 'done', or 'all'"
    ),
):
    """
    llm-todo list           # show pending
    llm-todo list done      # show only completed
    llm-todo list all       # show everything
    """
    # pick the right slice
    if which is None:
        tasks = list_tasks(include_completed=False)
    elif which.lower() == "done":
        # get everything, then filter to only completed
        tasks = [t for t in list_tasks(include_completed=True) if t["completed"]]
    elif which.lower() == "all":
        tasks = list_tasks(include_completed=True)
    else:
        typer.echo("❗️ Invalid argument. Use `done` or `all`.")
        raise typer.Exit(1)

    if not tasks:
        typer.echo("No tasks.")
        raise typer.Exit()

    # display with simple 1-based index
    for idx, t in enumerate(tasks, start=1):
        status = "✅" if t["completed"] else "❌"
        due = t.get("due") or ""
        typer.echo(f"{idx}. {status} {t['name']} (due: {due})")


@app.command()
def finish(task_parts: List[str] = typer.Argument(None)):
    """
    Mark a task as done. If no <n> provided, prompts you to pick one.
    """
    pending = list_tasks()
    if not pending:
        typer.echo("No pending tasks to finish.")
        raise typer.Exit()

    if not task_parts:
        # interactive
        for idx, t in enumerate(pending, start=1):
            typer.echo(f"{idx}. ❌ {t['name']}")
        choice = typer.prompt("Enter task number to finish")
    else:
        choice = task_parts[0]

    try:
        n = int(choice) - 1
        task_id = pending[n]["id"]
    except Exception:
        typer.echo("Invalid task number.")
        raise typer.Exit(1)

    result = finish_task(task_id)
    typer.echo(result["info"])


@app.command()
def remove(task_parts: List[str] = typer.Argument(None)):
    """
    Remove a task. If no <n> provided, prompts you to pick one.
    """
    pending = list_tasks()
    if not pending:
        typer.echo("No pending tasks to remove.")
        raise typer.Exit()

    if not task_parts:
        for idx, t in enumerate(pending, start=1):
            typer.echo(f"{idx}. ❌ {t['name']}")
        choice = typer.prompt("Enter task number to remove")
    else:
        choice = task_parts[0]

    try:
        n = int(choice) - 1
        task_id = pending[n]["id"]
    except Exception:
        typer.echo("Invalid task number.")
        raise typer.Exit(1)

    result = remove_task(task_id)
    typer.echo(result["info"])


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


if __name__ == "__main__":
    app()
