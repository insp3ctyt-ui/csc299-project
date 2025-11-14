import typer
import shlex  # For safely splitting shell-style input
from rich.console import Console
from typer.testing import CliRunner  # The key import for this prototype

from . import cli_tasks, cli_notes, cli_ai
from .database import create_db_and_tables

# Create the main 'app'
app = typer.Typer()

# Add the sub-commands from other files
app.add_typer(cli_tasks.app, name="tasks")
app.add_typer(cli_notes.app, name="notes")
app.add_typer(cli_ai.app, name="ai")

# Create a runner to call our app programmatically
runner = CliRunner()

def main():
    """
    The main entry point for the 'pkms' script.
    This function creates the chat-style REPL.
    """
    
    # This runs once when the app starts
    create_db_and_tables()
    
    console = Console()
    console.print("[bold green]Welcome to your Personal Knowledge & Task Manager![/bold green]")
    console.print("Type 'tasks list', 'notes add \"My note\"', or 'exit' to quit.")

    while True:
        try:
            # 1. Get user input from our custom prompt
            user_input = typer.prompt("pkms >")

            # 2. Check for exit command
            if user_input.strip().lower() in ("exit", "quit"):
                console.print("[bold cyan]Goodbye![/bold cyan]")
                break

            # 3. Parse the input into a list (like from a command line)
            # shlex.split handles quotes correctly, e.g., 'tasks add "My new task"'
            args = shlex.split(user_input)

            # 4. Run the command using the CliRunner
            if args:  # Only run if input was not empty
                result = runner.invoke(app, args)
                
                # 5. Print the output from the command
                if result.stdout:
                    # We strip the trailing newline that invoke() adds
                    # to keep the output clean.
                    console.print(result.stdout.strip())
                
                # 6. Handle errors (like 'task not found')
                # The error message is already in result.stdout
                if result.exit_code != 0:
                    pass # The error already printed, so just continue the loop

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            console.print("\n[bold cyan]Goodbye![/bold cyan]")
            break
        except Exception as e:
            # Catch any other unexpected errors (e.g., shlex parsing)
            console.print(f"[bold red]An unexpected error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()