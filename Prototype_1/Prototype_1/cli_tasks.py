import typer
from sqlmodel import Session, select
from typing_extensions import Annotated

from .database import Task, get_session

app = typer.Typer(help="Manage your tasks.")

@app.command(name="add")
def add_task(
    description: Annotated[str, typer.Argument(help="The task description.")]
):
    """Add a new task."""
    with next(get_session()) as session:
        task = Task(description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        print(f"Added task: {task.description}")

@app.command(name="list")
def list_tasks():
    """List all tasks."""
    with next(get_session()) as session:
        tasks = session.exec(select(Task)).all()
        if not tasks:
            print("No tasks found.")
            return
        
        print("--- Tasks ---")
        for task in tasks:
            print(f"[{task.id}] {task.description} ({task.status})")