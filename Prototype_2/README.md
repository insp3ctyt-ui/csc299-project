# Prototype 2: Expanded Features

This directory contains the second prototype of the PKMS and task management software for the CSC299 project.

This version iterates on Prototype 1 by adding:
* **Task Management:** New `done` and `delete` commands.
* **AI Agent:** A new `ai summarize` command that uses the OpenAI API.
* **Testing:** A `pytest` test suite for the task commands.

## Setup

This project is managed using `uv`.

1.  **Navigate to this directory:**
    ```bash
    cd Prototype_2
    ```

2.  **Install dependencies:**
    This command will create a local virtual environment (`.venv`) and install all required packages.
    ```bash
    uv pip install -e ".[dev]"
    ```
    *(Note: The quotes around `".[dev]"` are required for `zsh` users.)*

## How to Run

All commands must be run from this `Prototype_2` directory. The application is executed using `uv run pkms`.

**To see the main help menu:**
```bash
uv run pkms --help
```

## Task Commands

### `tasks list`: List all tasks

Lists all tasks and their outputs

**Example Input**

```bash
uv run pkms tasks list
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
uv run pkms tasks add "This is my new task description"
```
**Example Output**

```bash
Added task: This is my new task description
```

### `tasks done`: Mark a task as complete

Use the `done` command followed by the task's ID.

**Example Input:**

```bash
uv run pkms tasks done 2
```

**Example Output**

```
Completed task: [2] Add new features to the app
```

### `tasks delete`: Permanently delete a task

Use the `delete` command followed by the task's ID

**Example Input**

```bash
uv run pkms tasks delete 1
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
uv run pkms notes list
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
uv run pkms notes add "This is a new knowledge note."
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
uv run pkms ai summarize 2
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