# Final Product: Linked Data & AI Planning Agent

This directory contains the fourth prototype of the PKMS and task management software for the CSC299 project.

This version iterates on Prototype 3 by adding the final core features:
* **Data Linking:** Tasks can now be linked to notes using a foreign key in the database.
* **Search:** Added `search` commands for both tasks and notes.
* **AI Planning Agent:** A new `ai plan` command that reads a task (and its linked note) and generates a list of sub-tasks, which are then *automatically added* to the database.

## Setup

This project is managed using `uv`.

1.  **Navigate to this directory:**
    ```bash
    cd Prototype_4
    ```

2.  **Install dependencies:**
    This command will create a local virtual environment (`.venv`) and install all required packages.
    ```bash
    uv pip install -e ".[dev]"
    ```
    *(Note: The quotes around `".[dev]"` are required for `zsh` users.)*

## How to Run

All commands are run *inside* the application's interactive prompt.

1.  **Start the application:**
    From this `Prototype_4` directory, run:
    ```bash
    uv run pkms
    ```

2.  **Use the REPL:**
    You will be greeted with a welcome message and a `pkms >` prompt.
    ```
    Welcome to your Personal Knowledge & Task Manager!
    Type 'tasks list', 'notes add "My note"', or 'exit' to quit.
    pkms > 
    ```

3.  **Exit the application:**
    To quit the app, type `exit`.

## Task Commands

### `tasks list`

Lists all tasks and their status. Now shows note links.

**Example Input**

```bash
pkms > tasks list
```
**Example Output**

```bash
--- Tasks ---
[1] Write final project essay (todo) (links to Note 1)
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
### `tasks search`: Searches task description for a term

**Example Input:**

```bash
pkms > tasks search "essay"
```

**Example Output:**

```bash
--- Search Results for 'essay' ---
[1] Write final project essay (todo) (links to Note 1)
```

### `tasks link`: Links a task (by ID) to a note (by ID)

**Example Input:**

```bash
pkms > tasks link 1 1
```

**Example Output:**

```bash
Linked Task 1 to Note 1
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

### `notes search`: Searches note content for a term

**Example Input:**

```bash
pkms > notes search "AI"
```

**Example Output:**

```bash
--- Search Results for 'AI' ---
[1] My essay plan: 1. Intro to AI. 2. History...
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

### `ai plan`:

Reads a task (and its linked note) and generates sub-tasks, adding them to the database.

**Example Input:**

```bash
pkms > ai plan
```

**Example Output:**

```bash
1 Found task: Write final project essay Found linked note 1. Sending to AI for planning...

--- AI Plan ---
Adding sub-task: Draft introduction to AI and its impact. Adding sub-task: Research and write section on the history of LLMs. Adding sub-task: Formulate and write the conclusion.

Successfully added all sub-tasks to your task list.
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