import typer
from . import cli_tasks, cli_notes
from .database import create_db_and_tables

# Create the main 'app'
app = typer.Typer()

# Add the sub-commands from other files
app.add_typer(cli_tasks.app, name="tasks")
app.add_typer(cli_notes.app, name="notes")

def main():
    # This runs once when the app starts
    create_db_and_tables()
    app()

if __name__ == "__main__":
    main()