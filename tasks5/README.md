# CLI Task App

Single-file Python CLI that stores tasks in `data.json` at the project root.

Usage examples:

```bash
python cli_app.py add "Buy milk" --desc "2 liters"
python cli_app.py list
python cli_app.py update 1 --toggle
python cli_app.py get 1
python cli_app.py delete 1
```

The app is portable and self-contained. Requires Python 3.7+.
