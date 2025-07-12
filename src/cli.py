import typer
from typing import List

from utils import parse_task_parts
from core import add_task

app = typer.Typer()


@app.command()
def add(task_parts: List[str]):
    task = parse_task_parts(task_parts)
    result = add_task(task)
    typer.echo(result["info"])
