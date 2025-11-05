# tasks3 - PKMS/Task Software (v3)

This is the third iteration of the task management application, now structured as a formal Python package using `uv` and `pytest`.

## Setup

This project is managed with `uv`.

1.  **Install `uv`**:
    ```bash
    pip install uv
    ```

2.  **Install dependencies**:
    From this `tasks3` directory, run:
    ```bash
    uv add --dev pytest --no-workspace
    ```
    (You may also need to run `uv sync --no-workspace` to create the virtual environment)

## How to Run Tests

From the `tasks3` directory, run `pytest` using `uv`:

```bash
uv run pytest --no-workspace