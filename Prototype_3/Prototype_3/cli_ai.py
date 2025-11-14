import typer
from openai import OpenAI
from typing_extensions import Annotated

from .database import Note, get_session

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
    system_prompt = "You are an expert summarizer. Summarize the following note into a single, concise sentence."

    try:
        completion = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": note_content}
            ]
        )
        summary = completion.choices[0].message.content
        print("\n--- AI Summary ---")
        print(summary)
        print("--------------------")

    except Exception as e:
        print(f"An error occurred while contacting the OpenAI API: {e}")