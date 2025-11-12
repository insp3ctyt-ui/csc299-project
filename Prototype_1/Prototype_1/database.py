from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional

# 1. Define Your Data Models (the tables)
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: str = Field(index=True)
    status: str = "todo"

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str

# 2. Define the Database Engine
DATABASE_URL = "sqlite:///project.db"
engine = create_engine(DATABASE_URL)

# 3. Create the Database and Tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# 4. Define your "Session" (how you talk to the DB)
def get_session():
    with Session(engine) as session:
        yield session