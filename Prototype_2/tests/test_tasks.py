import pytest
from sqlmodel import Session, SQLModel, create_engine
from typer.testing import CliRunner

# --- Imports for Patching ---
from Prototype_2 import cli_tasks  # Import the module we need to patch
from Prototype_2.database import get_session as original_get_session # Store the original function

# --- Imports for Running ---
from Prototype_2 import app  # Import the main Typer app object
from Prototype_2.database import Task

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
#    to use the temporary test database instead
@pytest.fixture(autouse=True)
def override_get_session(session: Session):
    
    # Define a new getter function that is a GENERATOR,
    # just like our real one.
    def get_test_session():
        yield session

    # Patch cli_tasks with our new generator
    cli_tasks.get_session = get_test_session
    
    yield # The test runs here
    
    # After the test, we put the original function back
    cli_tasks.get_session = original_get_session

# 4. Finally, your tests (these are unchanged)
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