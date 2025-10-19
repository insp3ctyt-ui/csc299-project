# Tasks1 Prototype

This directory contains a simple command-line task management prototype for the CSC299 project.

## How to Run

All commands must be run from within the `tasks1` directory.

### `add`: Add a new task

Use the `add` command followed by a description of your task. The description can be multiple words.

**Example:**
```bash
python3 tasks.py add "Finish the 'Getting Started' assignment"
```

### `list`: see all current tasks
```bash
python3 tasks.py list


Example Output:

--- Your Tasks ---
[1] Finish the 'Getting Started' assignment
[2] Buy groceries for the week
------------------
```

### `search`: search for keywords/phrases in tasks

``` bash
python3 tasks.py search "assignment"

Example Output:

--- Search Results for 'assignment' ---
[1] Finish the 'Getting Started' assignment
---------------------------------------
```