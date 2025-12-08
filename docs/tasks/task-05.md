# Task 5: Database Setup with SQLModel

## Objectives
- Set up SQLModel ORM
- Create database connection and session management
- Initialize database schema

## Subtasks

### 5.1 Add SQLModel Dependency
- [ ] Add `sqlmodel>=0.0.14` to `pyproject.toml` dependencies

### 5.2 Create Database Module (`src/vibe_todo/database.py`)
- [ ] Import SQLModel, create_engine, Session
- [ ] Create `get_engine()` function with singleton pattern
- [ ] Configure SQLite connection string: `sqlite:///data/todos.db`
- [ ] Create `get_session()` context manager/generator
- [ ] Create `create_db_and_tables()` function
- [ ] Add error handling for database operations
- [ ] Integrate logger for database operations

### 5.3 Initialize Database in App
- [ ] Call `create_db_and_tables()` on app startup
- [ ] Add error handling for initialization
- [ ] Log database initialization status

## Acceptance Criteria
- ✅ SQLModel dependency installed
- ✅ Database engine created successfully
- ✅ Database file created in `data/` directory
- ✅ Session management works correctly
- ✅ Database operations logged

## Notes
- Use singleton pattern for engine to avoid multiple connections
- Session should be created per request/operation
- Database file should be created automatically
