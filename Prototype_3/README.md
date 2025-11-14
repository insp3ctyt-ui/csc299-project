# Prototype 3: Interactive Chat Interface

This directory contains the third prototype of the PKMS and task management software for the CSC299 project.

This version iterates on Prototype 2 by adding a **full terminal-based chat interface (REPL)**. Instead of running a separate command for each action, you now start the app once and type commands (like `tasks list` or `notes add`) into an interactive `pkms >` prompt.

All features from Prototype 2 (task management, note management, AI summarization, and testing) are still included.

## Setup

This project is managed using `uv`.

1.  **Navigate to this directory:**
    ```bash
    cd Prototype_3
    ```

2.  **Install dependencies:**
    This command will create a local virtual environment (`.venv`) and install all required packages.
    ```bash
    uv pip install -e ".[dev]"
    ```
    *(Note: The quotes around `".[dev]"` are required for `zsh` users.)*

## How to Run

All commands are now run *inside* the application's interactive prompt.

1.  **Start the application:**
    From this `Prototype_3` directory, run:
    ```bash
    uv run pkms
    ```

2.  **Use the REPL:**
    You will be greeted with a welcome message and a new prompt.
    ```
    Welcome to your Personal Knowledge & Task Manager!
    Type 'tasks list', 'notes add "My note"', or 'exit' to quit.
    pkms > 
    ```

3.  **Type commands:**
    You can now type all your commands directly into this prompt.
    ```
    pkms > tasks list
    pkms > notes add "My first note in the REPL"
    ```

4.  **Exit the application:**
    To quit the app, type `exit` or `quit`, or press `Ctrl+C`.
    ```
    pkms > exit
    Goodbye!
    ```

## Example Commands

All examples below are typed *inside* the `pkms >` prompt.

## Task Commands

### `tasks list`: List all tasks

Lists all tasks and their outputs

**Example Input**

```bash
pkms > tasks list
```
**Example Output**

```bash
--- Tasks ---
[1] Finish Sprint 1 of the project (todo)
------------------
```

### `tasks add`: Add a new task

Use the `add` command followed by a description of your task.

**Example Input**

```bash
pkms > tasks add "This is my new task description"
```
**Example Output**

```bash
Added task: This is my new task description
```

### `tasks done`: Mark a task as complete

Use the `done` command followed by the task's ID.

**Example Input:**

```bash
pkms > tasks done 2
```

**Example Output**

```
Completed task: [2] Add new features to the app
```

### `tasks delete`: Permanently delete a task

Use the `delete` command followed by the task's ID

**Example Input**

```bash
pkms > tasks delete 1
```

**Example Output**

```
Deleted task: [1] Finish Prototype 1 of the project
```

## Note Commands

### `notes list`: List all notes

Lists all notes

**Example Input**

```bash
pkms > notes list
```

**Example Output**

```bash
--- Notes ---
[1] This is a new knowledge note.
------------------
```

### `notes add`: Add a new note

Use the `add` command followed by the content of your note.

**Example Input**

```bash
pkms > notes add "This is a new knowledge note."
```

**Example Output**

```bash
Added note (ID: 1)
```

## AI Agent

### `ai summarize`: Summarize a note

Uses the OpenAI API (`gpt-5-nano`) to summarize a specific note by its ID.    

**Note:** You must set your API key as an environment variable in your terminal session before running this command.

**Example Input:**

```bash
# First, set the key
export OPENAI_API_KEY='sk-YourKeyHere...'

# Then, run the command
pkms > ai summarize 2
```

**Example Output:**

```bash
Welcome to your Personal Knowledge & Task Manager!
...
pkms > notes add "The OpenAI API is a powerful tool..."
Added note (ID: 2)

pkms > ai summarize 2
Fetching note 2...
Sending to AI for summarization...

--- AI Summary ---
The OpenAI API enables developers to easily incorporate...
--------------------
```

## Testing

This prototype includes a `pytest` test suite. The tests run against a temporary, in-memory database and do not affect your `project.db` file. The test suite does not use the REPL and tests the underlying commands directly.

**To run the tests:**

```bash
uv run python -m pytest
```

**Example Output:**

```
============================= test session starts ==============================
collected 3 items                                                              

tests/test_tasks.py ...                                                  [100%]

============================== 3 passed in 0.50s ===============================
```