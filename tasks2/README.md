# Tasks2 Iteration

This directory contains the second iteration of the command-line task management prototype for the CSC299 project.

This version adds the ability to **mark tasks as complete** and **delete tasks**.

## How to Run

All commands must be run from within the `tasks2` directory.

### `add`: Add a new task

Use the `add` command followed by a description of your task.

**Example:**
```bash
python3 tasks.py add "Develop new features for tasks app"
```

### `list`: see all current tasks

Lists all tasks and their status (`[ ]` for pending, `[X]` for completed).

```bash
python3 tasks.py list
```

**Example Output:**
```
--- Your Tasks ---
[X] [1] Finish the 'Getting Started' assignment
[ ] [2] Buy groceries for the week
[ ] [3] Develop new features for tasks app
------------------
```

### `search`: search for keywords/phrases in tasks

```bash
python3 tasks.py search "assignment"
```

**Example Output:**
```
--- Search Results for 'assignment' ---
[X] [1] Finish the 'Getting Started' assignment
---------------------------------------
```

### `done`: Mark a task as complete

Use the `done` command followed by the task's ID number.

```bash
python3 tasks.py done 2
```

**Example Output:**
```
Completed task: '[X] [2] Buy groceries for the week'
```

### `delete`: Permanently delete a task

Use the `delete` command followed by the task's ID number.

```bash
python3 tasks.py delete 1
```

**Example Output:**
```
Deleted task with ID 1.
```