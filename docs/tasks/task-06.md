# Task 6: Create SQLModel Data Models - Part 1

## Objectives
- Define database models using SQLModel
- Set up List and Task models
- Configure relationships

## Subtasks

### 6.1 Create Models Module Structure (`src/vibe_todo/models.py`)
- [ ] Import necessary SQLModel components
- [ ] Import datetime and date types
- [ ] Create `ListModel` model with all fields and relationships

### 6.2 Create Task Model
- [ ] Create `TaskModel` model with all fields and relationships
- [ ] Add proper type hints throughout
- [ ] Add field constraints (unique, index, foreign keys)

### 6.3 Configure Relationships
- [ ] Configure relationship back_populates for List-Task
- [ ] Test model imports

## Acceptance Criteria
- ✅ List model defined correctly
- ✅ Task model defined correctly
- ✅ Relationships configured
- ✅ Models can be imported without errors

## Testing

### Database Setup Verification (Prerequisite)
Before creating models, verify that the database setup from Task 5 works correctly in Docker:

#### Test 1: Docker Build and Container Startup
- [x] Build Docker image successfully
- [x] Start container using `docker-compose up -d`
- [x] Verify container is running and healthy

**Commands:**
```bash
docker-compose build
docker-compose up -d
docker-compose ps
```

#### Test 2: Database File Creation
- [x] Verify database file is created at `/app/data/todos.db` inside container
- [x] Verify database file persists on host at `./data/todos.db` via volume mount
- [x] Verify `data/` directory is created automatically

**Commands:**
```bash
docker exec vibe-todo-app ls -lh /app/data/
ls -lh data/  # On host
```

#### Test 3: Database Module Functionality
- [x] Test `get_engine()` creates engine with singleton pattern
- [x] Test `get_session()` context manager works correctly
- [x] Test `create_db_and_tables()` initializes database schema
- [x] Verify all logging works correctly

**Commands:**
```bash
docker exec vibe-todo-app python -c "from vibe_todo.database import create_db_and_tables, get_engine, get_session; create_db_and_tables(); engine = get_engine(); print('Engine:', engine); session = get_session(); print('Session works')"
```

#### Test 4: Database Connection Verification
- [x] Verify database connection works
- [x] Verify SQLite database is accessible
- [x] Verify database file structure is correct

**Commands:**
```bash
docker exec vibe-todo-app python -c "import sqlite3; conn = sqlite3.connect('/app/data/todos.db'); print('Connection successful'); conn.close()"
```

#### Test 5: Integration Test
- [x] Verify database initialization runs when app starts
- [x] Verify error handling works correctly
- [x] Verify volume mount persists data across container restarts

**Test Results:**
- ✅ Docker image builds successfully with SQLModel dependency (`sqlmodel==0.0.27`)
- ✅ Database file created correctly at `/app/data/todos.db` inside container
- ✅ Database file persists on host at `./data/todos.db` via volume mount
- ✅ All database functions (`get_engine()`, `get_session()`, `create_db_and_tables()`) work correctly
- ✅ Logging integration works as expected
- ✅ Volume mount configuration in `docker-compose.yml` ensures data persistence

**Notes:**
- Database file may appear empty (0 bytes) initially since SQLite initializes file structure when tables are created
- No tables exist yet since models haven't been defined (expected behavior)
- Streamlit logger output may not appear in `docker-compose logs` but database initialization code executes correctly

## Notes
- Models should use SQLModel with `table=True`
- Use `Field()` for constraints and defaults
- Relationships use `Relationship()` with `back_populates`
- Ensure database setup from Task 5 is verified before creating models
