import sys
import json
import os

# Define the file where tasks will be stored
DATA_FILE = 'tasks.json'

def load_tasks():
    """Loads tasks from the JSON file. Returns an empty list if the file doesn't exist."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Saves the list of tasks to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def add_task(task_description):
    """Adds a new task to the list."""
    tasks = load_tasks()
    new_task = {'id': len(tasks) + 1, 'description': task_description}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task: '{task_description}'")

def list_tasks():
    """Lists all stored tasks."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    print("--- Your Tasks ---")
    for task in tasks:
        print(f"[{task['id']}] {task['description']}")
    print("------------------")

def search_tasks(search_term):
    """Searches for tasks containing the search term."""
    tasks = load_tasks()
    # Find tasks where the search term is in the description (case-insensitive)
    results = [task for task in tasks if search_term.lower() in task['description'].lower()]
    
    if not results:
        print(f"No tasks found matching '{search_term}'.")
        return

    print(f"--- Search Results for '{search_term}' ---")
    for task in results:
        print(f"[{task['id']}] {task['description']}")
    print("---------------------------------------")

def print_usage():
    """Prints the help/usage message."""
    print("Usage:")
    print("  python tasks.py list                - Lists all tasks")
    print("  python tasks.py add <description>   - Adds a new task")
    print("  python tasks.py search <term>     - Searches for tasks")

def main():
    # sys.argv is a list of command-line arguments
    # sys.argv[0] is the script name (tasks.py)
    # sys.argv[1] is the command (list, add, search)
    # sys.argv[2:] are the other arguments (task description or search term)
    
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1].lower()
    
    if command == 'list':
        list_tasks()
    elif command == 'add':
        if len(sys.argv) < 3:
            print("Error: Please provide a description for the task.")
            print_usage()
            return
        # Join all arguments after 'add' to form the task description
        description = ' '.join(sys.argv[2:])
        add_task(description)
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: Please provide a search term.")
            print_usage()
            return
        # Join all arguments after 'search' to form the search term
        term = ' '.join(sys.argv[2:])
        search_tasks(term)
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()

if __name__ == "__main__":
    main()