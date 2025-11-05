import sys
import json
import os

# --- This is the test function from the setup ---
def inc(x: int) -> int:
    return x + 1
# --- End of test function ---


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
        print("Error: Could not decode tasks.json. Starting with an empty list.")
        return []

def save_tasks(tasks):
    """Saves the list of tasks to the JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def get_next_id(tasks):
    """Calculates the next unique ID."""
    if not tasks:
        return 1
    # Find the highest existing ID and add 1
    return max(task['id'] for task in tasks) + 1

def add_task(task_description):
    """Adds a new task to the list."""
    tasks = load_tasks()
    new_task = {
        'id': get_next_id(tasks),
        'description': task_description,
        'status': 'pending'
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Added task: '[ ] [{new_task['id']}] {task_description}'")
    return new_task['id'] # Return the new ID for testing

def list_tasks():
    """Lists all stored tasks with their status."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    
    print("--- Your Tasks ---")
    for task in tasks:
        status = task.get('status', 'pending') 
        marker = '[X]' if status == 'completed' else '[ ]'
        print(f"{marker} [{task['id']}] {task['description']}")
    print("------------------")

def search_tasks(search_term):
    """Searches for tasks containing the search term."""
    tasks = load_tasks()
    results = [task for task in tasks if search_term.lower() in task['description'].lower()]
    
    if not results:
        print(f"No tasks found matching '{search_term}'.")
        return

    print(f"--- Search Results for '{search_term}' ---")
    for task in results:
        status = task.get('status', 'pending')
        marker = '[X]' if status == 'completed' else '[ ]'
        print(f"{marker} [{task['id']}] {task['description']}")
    print("---------------------------------------")

def mark_task_done(task_id):
    """Marks a specific task as 'completed'."""
    tasks = load_tasks()
    task_found = False
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = 'completed'
            save_tasks(tasks)
            print(f"Completed task: '[X] [{task['id']}] {task['description']}'")
            task_found = True
            break
    
    if not task_found:
        print(f"Error: Task with ID {task_id} not found.")

def delete_task(task_id):
    """Deletes a specific task from the list."""
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task['id'] != task_id]
    
    if len(new_tasks) == len(tasks):
        print(f"Error: Task with ID {task_id} not found.")
    else:
        save_tasks(new_tasks)
        print(f"Deleted task with ID {task_id}.")

def print_usage():
    """Prints the help/usage message."""
    print("Usage:")
    print("  uv run tasks3 list                - Lists all tasks")
    print("  uv run tasks3 add <description>   - Adds a new task")
    print("  uv run tasks3 search <term>     - Searches for tasks")
    print("  uv run tasks3 done <id>         - Marks a task as complete")
    print("  uv run tasks3 delete <id>       - Deletes a task")

def main():
    """Main entry point for the application."""
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
        description = ' '.join(sys.argv[2:])
        add_task(description)
    elif command == 'search':
        if len(sys.argv) < 3:
            print("Error: Please provide a search term.")
            print_usage()
            return
        term = ' '.join(sys.argv[2:])
        search_tasks(term)
    
    elif command == 'done' or command == 'delete':
        if len(sys.argv) < 3:
            print(f"Error: Please provide a task ID for the '{command}' command.")
            print_usage()
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("Error: Task ID must be a number.")
            return
        
        if command == 'done':
            mark_task_done(task_id)
        elif command == 'delete':
            delete_task(task_id)
            
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()