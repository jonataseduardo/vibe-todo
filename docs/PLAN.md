# Todo App Development Plan

## Overview
Build a Microsoft TODO-like application using Streamlit with SQLite database backend, using SQLModel as the ORM.

## Project Structure
```
vibe-todo/
├── app.py                    # Streamlit application entry point
├── src/
│   └── vibe_todo/
│       ├── __init__.py
│       ├── database.py      # SQLModel engine and session management
│       ├── models.py         # SQLModel table models
│       └── services.py       # Business logic layer using SQLModel sessions
├── data/
│   └── todos.db             # SQLite database file (gitignored)
└── tests/
    └── test_vibe_todo.py
```

## Core Features (Microsoft TODO-like)

### 1. Task Lists
- Create, rename, delete task lists
- Each list can contain multiple tasks
- Default lists: "My Day", "Important", "Planned", "Tasks"

### 2. Tasks
- **Basic Properties:**
  - Title (required)
  - Description/Notes (optional)
  - Due date (optional)
  - Completion status
  - Created date
  - Last modified date
  
- **Advanced Properties:**
  - Priority/Important flag
  - Subtasks (optional)
  - List assignment

### 3. Views
- **My Day**: Tasks added to "My Day" view
- **Important**: Tasks marked as important
- **Planned**: Tasks with due dates
- **Tasks**: All tasks across all lists
- **Custom Lists**: User-created lists

### 4. Task Operations
- Create new tasks
- Edit existing tasks
- Delete tasks
- Mark complete/incomplete
- Toggle "Important" flag
- Add/remove from "My Day"
- Assign to lists
- Add subtasks

## Implementation Steps

### Phase 1: Project Setup & Dependencies
1. **Update `pyproject.toml`**
   - Add `streamlit` dependency
   - Add `sqlmodel` dependency (includes SQLAlchemy)
   - Add `python-dateutil` for date handling (optional but helpful)

2. **Create database directory**
   - Create `data/` directory for SQLite database
   - Add `data/` to `.gitignore` (already done)

### Phase 2: Database Layer (`src/vibe_todo/database.py`)
1. **SQLModel Engine Setup**
   - Create SQLModel engine pointing to SQLite database
   - Database file location: `data/todos.db`
   - Configure connection string: `sqlite:///data/todos.db`
   - Create function to get engine: `get_engine() -> Engine`
   - Create function to create tables: `create_db_and_tables()`
   - Create session dependency: `get_session()` context manager or generator

2. **Database Initialization**
   - Initialize database on first run
   - Create all tables using SQLModel's `SQLModel.metadata.create_all()`
   - Seed default system lists if they don't exist

### Phase 3: Models Layer (`src/vibe_todo/models.py`)
1. **SQLModel Table Models**
   - All models inherit from `SQLModel` with `table=True`
   - Use SQLModel's type hints for field definitions
   - Define relationships using SQLModel's relationship features

2. **Model Definitions**
   
   **`List` Model:**
   ```python
   class List(SQLModel, table=True):
       id: int | None = Field(default=None, primary_key=True)
       name: str = Field(unique=True, index=True)
       created_at: datetime = Field(default_factory=datetime.now)
       is_system: bool = Field(default=False)
       tasks: list["Task"] = Relationship(back_populates="list")
   ```
   
   **`Task` Model:**
   ```python
   class Task(SQLModel, table=True):
       id: int | None = Field(default=None, primary_key=True)
       list_id: int = Field(foreign_key="list.id")
       title: str
       description: str | None = None
       due_date: date | None = None
       is_completed: bool = Field(default=False)
       is_important: bool = Field(default=False)
       created_at: datetime = Field(default_factory=datetime.now)
       updated_at: datetime = Field(default_factory=datetime.now)
       list: List = Relationship(back_populates="tasks")
       subtasks: list["Subtask"] = Relationship(back_populates="task")
       my_day_entries: list["MyDayTask"] = Relationship(back_populates="task")
   ```
   
   **`Subtask` Model:**
   ```python
   class Subtask(SQLModel, table=True):
       id: int | None = Field(default=None, primary_key=True)
       task_id: int = Field(foreign_key="task.id")
       title: str
       is_completed: bool = Field(default=False)
       created_at: datetime = Field(default_factory=datetime.now)
       task: Task = Relationship(back_populates="subtasks")
   ```
   
   **`MyDayTask` Model (many-to-many):**
   ```python
   class MyDayTask(SQLModel, table=True):
       task_id: int = Field(foreign_key="task.id", primary_key=True)
       date: date = Field(primary_key=True)
       task: Task = Relationship(back_populates="my_day_entries")
   ```

3. **Model Features**
   - Use SQLModel's `Field()` for constraints, defaults, and metadata
   - Leverage SQLModel's automatic type conversion
   - Use relationships for foreign keys
   - Add indexes for frequently queried fields (name, due_date, is_completed, etc.)

### Phase 4: Services Layer (`src/vibe_todo/services.py`)
1. **Session Management**
   - Use SQLModel sessions for all database operations
   - Create helper function `get_session()` that yields a session
   - Use context managers or dependency injection pattern
   - Ensure proper session cleanup

2. **List Services**
   - `create_list(name: str, session: Session) -> List`
   - `get_all_lists(session: Session) -> List[List]`
   - `get_list_by_id(list_id: int, session: Session) -> List | None`
   - `update_list(list_id: int, name: str, session: Session) -> List`
   - `delete_list(list_id: int, session: Session) -> bool`
   - `get_system_lists(session: Session) -> List[List]`
   - `get_or_create_system_list(name: str, session: Session) -> List`

3. **Task Services**
   - `create_task(list_id: int, title: str, session: Session, **kwargs) -> Task`
   - `get_tasks_by_list(list_id: int, session: Session) -> List[Task]`
   - `get_task_by_id(task_id: int, session: Session) -> Task | None`
   - `update_task(task_id: int, session: Session, **kwargs) -> Task`
   - `delete_task(task_id: int, session: Session) -> bool`
   - `toggle_complete(task_id: int, session: Session) -> Task`
   - `toggle_important(task_id: int, session: Session) -> Task`
   - `get_important_tasks(session: Session) -> List[Task]`
   - `get_planned_tasks(session: Session) -> List[Task]`
   - `get_my_day_tasks(date: date, session: Session) -> List[Task]`
   - `add_to_my_day(task_id: int, date: date, session: Session) -> MyDayTask`
   - `remove_from_my_day(task_id: int, date: date, session: Session) -> bool`
   - `get_all_tasks(session: Session, filters: dict | None = None) -> List[Task]`

4. **Subtask Services**
   - `create_subtask(task_id: int, title: str, session: Session) -> Subtask`
   - `get_subtasks_by_task(task_id: int, session: Session) -> List[Subtask]`
   - `toggle_subtask_complete(subtask_id: int, session: Session) -> Subtask`
   - `delete_subtask(subtask_id: int, session: Session) -> bool`

5. **Query Patterns**
   - Use SQLModel's query builder: `session.exec(select(Model))`
   - Use `where()` for filtering
   - Use `order_by()` for sorting
   - Leverage relationships for joins: `session.get(Task, task_id)` automatically loads relationships
   - Use eager loading when needed: `selectinload()` or `joinedload()`

### Phase 5: Streamlit UI (`app.py`)
1. **Page Structure**
   - Sidebar navigation:
     - My Day
     - Important
     - Planned
     - Tasks (All)
     - Custom Lists (dynamic)
     - Add New List button
   
2. **Database Session Management in Streamlit**
   - Create session per request/page load
   - Use `st.cache_resource` for engine (singleton)
   - Use context managers for sessions in each operation
   - Example pattern:
     ```python
     @st.cache_resource
     def get_db_engine():
         return get_engine()
     
     with Session(get_db_engine()) as session:
         # Use session for operations
     ```

3. **My Day View**
   - Show tasks added to today's "My Day"
   - Add task to My Day button
   - Task cards with completion toggle, important flag
   
4. **Important View**
   - Show all tasks marked as important
   - Filter by completion status
   
5. **Planned View**
   - Show tasks with due dates
   - Group by date (Today, Tomorrow, This Week, Later)
   - Calendar view option
   
6. **Tasks View**
   - Show all tasks
   - Filter by list, completion status, important
   - Search functionality
   
7. **List View**
   - Show tasks in selected list
   - Create new task in list
   - Edit/delete list
   
8. **Task Components**
   - Task card component:
     - Title (editable)
     - Description (editable)
     - Due date picker
     - Important toggle (star icon)
     - Complete checkbox
     - Add to My Day button
     - Subtasks section
     - Delete button
   
9. **Create Task Modal/Form**
   - Title input
   - Description textarea
   - List selector
   - Due date picker
   - Important checkbox
   - Add to My Day checkbox

### Phase 6: UI/UX Enhancements
1. **Styling**
   - Use Streamlit's built-in styling
   - Custom CSS for better appearance
   - Icons for actions (using emojis or streamlit-option-menu)
   
2. **State Management**
   - Use `st.session_state` for:
     - Current view
     - Selected list
     - Task filters
     - UI state (modals, expanded tasks)
   
3. **User Experience**
   - Confirmation dialogs for deletions
   - Success/error messages
   - Loading states
   - Empty state messages

### Phase 7: Testing
1. **Unit Tests** (`tests/test_vibe_todo.py`)
   - Test SQLModel models
   - Test service functions with test database
   - Use in-memory SQLite database for tests: `sqlite:///:memory:`
   - Test relationships and queries
   
2. **Integration Tests**
   - Test Streamlit app flows
   - Test database persistence
   - Test session management

### Phase 8: Documentation & Polish
1. **Update README.md**
   - Installation instructions
   - Usage guide
   - Features list
   
2. **Code Documentation**
   - Docstrings for all functions
   - Type hints throughout (SQLModel provides excellent type hints)
   
3. **Error Handling**
   - SQLModel/SQLAlchemy error handling
   - User input validation
   - Graceful error messages
   - Transaction rollback on errors

## Technical Considerations

### SQLModel ORM
- **Benefits:**
  - Type-safe database operations
  - Automatic schema generation from models
  - Pydantic validation built-in
  - Relationship management
  - Query builder with type hints
  
- **Engine Management:**
  - Create engine once and reuse (use `st.cache_resource` in Streamlit)
  - Use connection pooling (SQLModel handles this automatically)
  - Database file location: `data/todos.db`
  
- **Session Management:**
  - Create session per operation or request
  - Use context managers for automatic cleanup
  - Commit transactions explicitly
  - Handle rollbacks on errors
  
- **Migrations:**
  - SQLModel can create tables automatically
  - For future migrations, consider Alembic integration
  - Current approach: `SQLModel.metadata.create_all(engine)`

### Streamlit Best Practices
- Use `st.cache_resource` for database engine (singleton)
- Use `st.cache_data` carefully with database queries (may need to invalidate)
- Use `st.session_state` for state management
- Organize UI into functions/components
- Use columns for layout
- Implement proper form handling
- Handle database sessions properly (create/close per operation)

### Code Organization
- Separation of concerns: database → models → services → UI
- Type hints throughout (SQLModel provides excellent type inference)
- Error handling at each layer
- Logging for debugging
- Use SQLModel's validation features

### SQLModel Query Examples
```python
# Select all tasks
tasks = session.exec(select(Task)).all()

# Filter tasks
tasks = session.exec(
    select(Task).where(Task.is_completed == False)
).all()

# Get task with relationships
task = session.get(Task, task_id)  # Automatically loads relationships

# Join query
tasks = session.exec(
    select(Task, List)
    .join(List)
    .where(List.name == "My Day")
).all()

# Create and commit
task = Task(title="New Task", list_id=1)
session.add(task)
session.commit()
session.refresh(task)  # Refresh to get generated ID
```

## Dependencies Summary
```toml
dependencies = [
    "streamlit>=1.28.0",
    "sqlmodel>=0.0.14",  # SQLModel ORM (includes SQLAlchemy)
    "python-dateutil>=2.8.0",  # Optional but helpful for date parsing
]
```

## SQLModel-Specific Implementation Details

### Database Connection Pattern
```python
# database.py
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

engine = None

def get_engine() -> Engine:
    global engine
    if engine is None:
        engine = create_engine("sqlite:///data/todos.db", echo=False)
    return engine

def get_session() -> Generator[Session, None, None]:
    with Session(get_engine()) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())
```

### Model Definition Pattern
```python
# models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, date
from typing import Optional, List

class List(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    is_system: bool = Field(default=False)
    tasks: List["Task"] = Relationship(back_populates="list")
```

### Service Pattern
```python
# services.py
from sqlmodel import Session, select
from vibe_todo.models import Task, TodoList

def create_task(list_id: int, title: str, session: Session, **kwargs) -> Task:
    task = Task(list_id=list_id, title=title, **kwargs)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks_by_list(list_id: int, session: Session) -> List[Task]:
    statement = select(Task).where(Task.list_id == list_id)
    return list(session.exec(statement).all())
```

## Future Enhancements (Post-MVP)
- Task search functionality
- Task tags/categories
- Recurring tasks
- Task attachments
- Dark mode
- Export/import functionality
- User authentication (multi-user support)
- Task templates
- Statistics/analytics dashboard
- Database migrations with Alembic
- Advanced query optimization
- Full-text search with SQLite FTS
