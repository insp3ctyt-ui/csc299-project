import typer
from sqlmodel import Session, select
from typing_extensions import Annotated

from .database import Note, get_session

app = typer.Typer(help="Manage your knowledge notes.")

@app.command(name="add")
def add_note(
    content: Annotated[str, typer.Argument(help="The content of the note.")]
):
    """Add a new note."""
    with next(get_session()) as session:
        note = Note(content=content)
        session.add(note)
        session.commit()
        session.refresh(note)
        print(f"Added note (ID: {note.id})")

@app.command(name="list")
def list_notes():
    """List all notes."""
    with next(get_session()) as session:
        notes = session.exec(select(Note)).all()
        if not notes:
            print("No notes found.")
            return
        
        print("--- Notes ---")
        for note in notes:
            print(f"[{note.id}] {note.content[:50]}...")