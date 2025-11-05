import pytest
import os
import json
from tasks3 import add_task, list_tasks, mark_task_done, delete_task

# This is a 'fixture'
# It runs before each test that asks for it
@pytest.fixture
def temp_tasks_file(monkeypatch, tmp_path):
    """
    Creates a temporary tasks.json file for each test,
    so tests don't interfere with each other or your real data.
    """
    # 1. Create a temp file path
    temp_file = tmp_path / "test_tasks.json"
    
    # 2. Use 'monkeypatch' to change the global DATA_FILE constant
    #    inside your 'tasks3' module to point to this temp file.
    monkeypatch.setattr("tasks3.DATA_FILE", str(temp_file))
    
    # 3. 'yield' control back to the test
    yield str(temp_file)
    
    # 4. (After test) Clean up if needed (tmp_path does this mostly)
    if os.path.exists(temp_file):
        os.remove(temp_file)


# --- Test 1: Test adding and listing a task ---
def test_add_and_list_task(temp_tasks_file, capsys):
    """
    Tests adding one task and then listing it.
    It checks both the file system and the console output.
    """
    # 1. ARRANGE (temp_tasks_file fixture has already run)
    
    # 2. ACT
    add_task("This is test task 1")
    
    # 3. ASSERT (Check the file)
    with open(temp_tasks_file, 'r') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]['description'] == "This is test task 1"
        assert data[0]['status'] == "pending"

    # 4. ACT (List the tasks)
    list_tasks()
    
    # 5. ASSERT (Check the captured stdout)
    captured = capsys.readouterr()
    assert "[ ] [1] This is test task 1" in captured.out
    assert "--- Your Tasks ---" in captured.out


# --- Test 2: Test marking a task as done ---
def test_mark_task_done(temp_tasks_file, capsys):
    """
    Tests adding a task and then marking it as complete.
    """
    # 1. ARRANGE
    # Add a task to work with (ID will be 1)
    new_id = add_task("Task to be completed")
    
    # 2. ACT
    mark_task_done(new_id)
    
    # 3. ASSERT (Check the file)
    with open(temp_tasks_file, 'r') as f:
        data = json.load(f)
        assert data[0]['status'] == "completed"

    # 4. ACT (List tasks to check the output)
    list_tasks()
    
    # 5. ASSERT (Check the captured stdout)
    captured = capsys.readouterr()
    assert "[X] [1] Task to be completed" in captured.out

# --- Test 3 (Bonus): Test deleting a task ---
def test_delete_task(temp_tasks_file, capsys):
    """
    Tests adding two tasks and deleting one.
    """
    # 1. ARRANGE
    id_to_keep = add_task("Keep this task")
    id_to_delete = add_task("Delete this task")
    
    # 2. ACT
    delete_task(id_to_delete)
    
    # 3. ASSERT (Check file)
    with open(temp_tasks_file, 'r') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]['id'] == id_to_keep

    # 4. ACT (List)
    
    # ---- THIS IS THE FIX ----
    # Clear the capture buffer of everything printed so far
    # (i.e., from the 'add_task' and 'delete_task' calls)
    capsys.readouterr() 
    # -------------------------
    
    list_tasks()
    
    # 5. ASSERT (Check output)
    # Now, 'captured' will *only* contain the output from 'list_tasks()'
    captured = capsys.readouterr() 
    assert "Keep this task" in captured.out
    assert "Delete this task" not in captured.out