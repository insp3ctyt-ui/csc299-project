# Prototype 1: Core PKMS Application

This directory contains the first prototype of the PKMS and task management software for the CSC299 project.

This version establishes the core application structure using `uv`, `typer`, and `sqlmodel`. It includes core features for **Task Management** (add, list) and **Note Management** (add, list). Data is stored in a local `project.db` SQLite file.

## Setup

This project is managed using `uv`.

1.  **Navigate to this directory:**
    ```bash
    cd Prototype_1
    ```

2.  **Install dependencies:**
    This command will create a local virtual environment (`.venv`) and install all required packages.
    ```bash
    uv pip install -e ".[dev]"
    ```
    *(Note: The quotes around `".[dev]"` are required for `zsh` users.)*

## How to Run

All commands must be run from this `Prototype_1` directory. The application is executed using `uv run pkms`.

**To see the main help menu:**
```bash
uv run pkms --help
```

## Commands

### 'tasks list': List all tasks

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

### 'tasks add': Add a new task

Use the 'add' command followed by a description of your task.

**Example Input**

```bash
uv run pkms tasks add "This is my new task description"
```
**Example Output**

```bash
Added task: This is my new task description
```

### 'notes list': List all notes

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

### 'notes add': Add a new note

Use the 'add' command followed by the content of your note.

**Example Input**

```bash
uv run pkms notes add "This is a new knowledge note."
```

**Example Output**

```bash
Added note (ID: 1)
```