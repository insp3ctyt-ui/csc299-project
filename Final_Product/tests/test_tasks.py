import pytest
from sqlmodel import Session, SQLModel, create_engine
from typer.testing import CliRunner

# --- Imports for Patching (Updated) ---
from Final_Product import cli_tasks  # Import the module we need to patch
from Final_Product.database import get_session as original_get_session # Store the original

# --- Imports for Running (Updated) ---
from Final_Product import app  # Import the main Typer app object
from Final_Product.database import Task

# 1. Create a "CliRunner" to simulate running your app
runner = CliRunner()

# 2. This is the magic: A "pytest fixture" to create a temporary DB
@pytest.fixture(name="session")
def session_fixture():
    # Use an in-memory-only database for testing
    engine = create_engine("sqlite:///:memory:") 
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# 3. This "overrides" your app's 'get_session' function
@pytest.fixture(autouse=True)
def override_get_session(session: Session):
    
    # Define a new getter function that is a GENERATOR
    def get_test_session():
        yield session

    # Patch cli_tasks with our new generator
    cli_tasks.get_session = get_test_session
    
    yield # The test runs here
    
    # After the test, put the original function back
    cli_tasks.get_session = original_get_session

# 4. Your updated tests
def test_add_task():
    result = runner.invoke(app, ["tasks", "add", "Test task"])
    
    assert result.exit_code == 0
    assert "Added task: Test task" in result.stdout

def test_list_tasks(session: Session):
    task = Task(description="My test list task")
    session.add(task)
    session.commit()

    result = runner.invoke(app, ["tasks", "list"])
    
    assert result.exit_code == 0
    assert "My test list task" in result.stdout

def test_list_tasks_empty():
    result = runner.invoke(app, ["tasks", "list"])
    
    assert result.exit_code == 0
    assert "No tasks found" in result.stdout

def test_done_task(session: Session):
    # Add a task to the DB first
    task = Task(description="Task to be done")
    session.add(task)
    session.commit()
    
    # Run the 'done' command
    result = runner.invoke(app, ["tasks", "done", "1"])
    
    assert result.exit_code == 0
    assert "Completed task: [1] Task to be done" in result.stdout
    
    # Verify it in the database
    task_from_db = session.get(Task, 1)
    assert task_from_db is not None
    assert task_from_db.status == "done"

def test_delete_task(session: Session):
    # Add a task to the DB first
    task = Task(description="Task to delete")
    session.add(task)
    session.commit()
    
    # Run the 'delete' command
    result = runner.invoke(app, ["tasks", "delete", "1"])
    
    assert result.exit_code == 0
    assert "Deleted task: [1] Task to delete" in result.stdout
    
    # Verify it's gone from the database
    task_in_db = session.get(Task, 1)
    assert task_in_db is None