import typer
from sqlmodel import Session, select
from typing_extensions import Annotated
from .database import Task, Note, get_session

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
            # --- NEW: Check for a link and display it ---
            link_info = f" (links to Note {task.note_id})" if task.note_id else ""
            print(f"[{task.id}] {task.description} ({task.status}){link_info}")

@app.command(name="done")
def complete_task(
    task_id: Annotated[int, typer.Argument(help="The ID of the task to mark as complete.")]
):
    """Mark a task as complete."""
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            raise typer.Exit(code=1)
        
        task.status = "done"
        session.add(task)
        session.commit()
        session.refresh(task)
        print(f"Completed task: [{task.id}] {task.description}")

@app.command(name="delete")
def delete_task(
    task_id: Annotated[int, typer.Argument(help="The ID of the task to delete.")]
):
    """Delete a task."""
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            raise typer.Exit(code=1)
        
        session.delete(task)
        session.commit()
        print(f"Deleted task: [{task.id}] {task.description}")

@app.command(name="link")
def link_task_to_note(
    task_id: Annotated[int, typer.Argument(help="The ID of the task.")],
    note_id: Annotated[int, typer.Argument(help="The ID of the note to link.")],
):
    """Link a task to a note."""
    with next(get_session()) as session:
        task = session.get(Task, task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            raise typer.Exit(code=1)

        note = session.get(Note, note_id) # Use string name for cross-file model
        if not note:
            print(f"Error: Note with ID {note_id} not found.")
            raise typer.Exit(code=1)

        task.note_id = note_id
        session.add(task)
        session.commit()
        session.refresh(task)
        print(f"Linked Task {task_id} to Note {note_id}")

@app.command(name="search")
def search_tasks(
    term: Annotated[str, typer.Argument(help="The text to search for.")]
):
    """Search tasks for a specific term."""
    with next(get_session()) as session:
        # Use .where() and .like() for a SQL-style search
        search_pattern = f"%{term}%"
        tasks = session.exec(select(Task).where(Task.description.like(search_pattern))).all()

        if not tasks:
            print(f"No tasks found matching '{term}'.")
            return

        print(f"--- Search Results for '{term}' ---")
        for task in tasks:
            print(f"[{task.id}] {task.description} ({task.status})")