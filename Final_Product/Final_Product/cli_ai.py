import typer
from openai import OpenAI
from typing_extensions import Annotated
import json  # Added for the new plan function
from sqlmodel import Session  # Added for the new plan function

# Import all models and the session getter
from .database import Note, Task, get_session

app = typer.Typer(help="Use AI agents to interact with your data.")


@app.command(name="summarize")
def ai_summarize_note(
    note_id: Annotated[int, typer.Argument(help="The ID of the note to summarize.")]
):
    """Summarize a note using the OpenAI API."""

    print(f"Fetching note {note_id}...")

    # 1. Get the note from the database
    with next(get_session()) as session:
        note = session.get(Note, note_id)
        if not note:
            print(f"Error: Note with ID {note_id} not found.")
            raise typer.Exit(code=1)

        if len(note.content) < 50:
            print("Note is too short to summarize. Aborting.")
            return

        note_content = note.content

    # 2. Get OpenAI API client (it checks for the environment variable)
    try:
        client = OpenAI()
        if not client.api_key:
            print("Error: OPENAI_API_KEY environment variable not set.")
            raise typer.Exit(code=1)
    except Exception as e:
        print(f"Error initializing OpenAI: {e}")
        raise typer.Exit(code=1)

    # 3. Send to API (just like in tasks4)
    print("Sending to AI for summarization...")
    system_prompt = (
        "You are an expert summarizer. Summarize the following note into a single, concise sentence."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": note_content},
            ],
        )
        summary = completion.choices[0].message.content
        print("\n--- AI Summary ---")
        print(summary)
        print("--------------------")

    except Exception as e:
        print(f"An error occurred while contacting the OpenAI API: {e}")


@app.command(name="plan")
def ai_plan_task(
    task_id: Annotated[int, typer.Argument(help="The ID of the task to plan.")]
):
    """Asks an AI agent to break a task down into sub-tasks."""

    # --- THIS IS THE FIX ---
    # We get the session manually, just like in the summarize command
    with next(get_session()) as session:
        # 1. Get the task from the database
        task = session.get(Task, task_id)
        if not task:
            print(f"Error: Task with ID {task_id} not found.")
            raise typer.Exit(code=1)

        print(f"Found task: {task.description}")

        # 2. Get the linked note, if it exists
        note_content = ""
        if task.note_id:
            note = session.get(Note, task.note_id)
            if note:
                note_content = note.content
                print(f"Found linked note {task.note_id}.")

        # 3. Get OpenAI API client
        try:
            client = OpenAI()
            if not client.api_key:
                print("Error: OPENAI_API_KEY environment variable not set.")
                raise typer.Exit(code=1)
        except Exception as e:
            print(f"Error initializing OpenAI: {e}")
            raise typer.Exit(code=1)

        # 4. Build a powerful prompt for the AI
        system_prompt = (
            "You are an expert planning assistant. Your job is to break a "
            "complex task down into a list of 3-5 smaller, actionable sub-tasks. "
            "You MUST return the sub-tasks as a JSON list of strings, "
            "and nothing else. Example: [\"Sub-task 1\", \"Sub-task 2\"]"
        )

        user_prompt = f"Main Task: {task.description}\n"
        if note_content:
            user_prompt += f"\nRelated Notes: {note_content}\n"
        user_prompt += "\nBreak this down into sub-tasks:"

        # 5. Send to API
        print("Sending to AI for planning...")
        try:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},  # Force JSON output
            )

            response_text = completion.choices[0].message.content
            sub_tasks = json.loads(response_text)

            # Check if it's a list or a dict {'sub-tasks': [...]}
            if isinstance(sub_tasks, dict):
                key = next(iter(sub_tasks))  # Get the first key, e.g., "sub-tasks"
                sub_tasks = sub_tasks[key]

            if not isinstance(sub_tasks, list):
                raise Exception("AI did not return a list.")

            # 6. THIS IS THE "AGENT" PART: Add sub-tasks to the database
            print("\n--- AI Plan ---")
            for sub_task_desc in sub_tasks:
                new_task = Task(
                    description=f"(Sub-task for {task_id}) {sub_task_desc}"
                )
                session.add(new_task)
                print(f"Adding sub-task: {sub_task_desc}")

            session.commit()
            print("\nSuccessfully added all sub-tasks to your task list.")

        except Exception as e:
            print(f"An error occurred while processing the AI response: {e}")