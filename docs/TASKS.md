# Todo App Development Tasks

> **Note**: This file has been split into individual task files. See the `tasks/` directory for detailed task breakdowns.
> 
> Each task is now in its own file (`task-XX.md`) with at most 3 subtasks per task for better focus and tracking.
> 
> See `tasks/README.md` for the complete task index.

## Quick Overview

Tasks have been organized into 33 individual files, each containing at most 3 subtasks. This makes it easier to:
- Focus on one small task at a time
- Track progress more granularly
- Understand dependencies
- Complete tasks incrementally

## Task Categories

1. **Environment Setup** (Tasks 1-4): Docker, logger, hello world app
2. **Database & Models** (Tasks 5-7): SQLModel setup and data models
3. **Services Layer** (Tasks 8-13): Business logic and CRUD operations
4. **UI Foundation** (Tasks 14-15): Streamlit app structure
5. **UI Views** (Tasks 16-21): Different views (My Day, Important, Planned, etc.)
6. **List & Task Management** (Tasks 22-26): CRUD UI for lists and tasks
7. **UI/UX Enhancements** (Tasks 27-28): Styling and user experience
8. **Testing** (Tasks 29-31): Unit, integration, and UI tests
9. **Documentation & Polish** (Tasks 32-33): Final documentation and cleanup

## Getting Started

1. Start with `tasks/task-01.md`
2. Complete tasks sequentially (1-33)
3. Check off subtasks as you complete them
4. Verify acceptance criteria before moving on

For detailed task information, see individual files in the `tasks/` directory.

---

## Original Task Breakdown (Reference)

The following is the original task breakdown kept for reference. For current tasks, see `tasks/` directory.

## Task 1: Environment Setup & Hello World App

### Objectives
- Set up Docker environment for local development
- Create a hello world Streamlit app
- Set up logging module using loguru
- Configure debug mode for local execution

### Subtasks

#### 1.1 Update Dependencies (`pyproject.toml`)
- [ ] Add `streamlit>=1.28.0` to dependencies
- [ ] Add `loguru>=0.7.0` to dependencies
- [ ] Add `python-dateutil>=2.8.0` to dependencies (optional but helpful)

#### 1.2 Create Logger Module (`src/vibe_todo/logger.py`)
- [ ] Create logger configuration using loguru
- [ ] Set up log levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Configure log format with timestamps and context
- [ ] Create log file rotation (optional)
- [ ] Export logger instance for use across the app
- [ ] Add function to configure logger based on environment (dev/prod)

#### 1.3 Create Hello World Streamlit App (`app.py`)
- [ ] Create basic Streamlit app structure
- [ ] Add hello world content
- [ ] Import and use logger module
- [ ] Add basic page title and header
- [ ] Test that app runs successfully

#### 1.4 Create Dockerfile
- [ ] Use Python 3.13 base image
- [ ] Set working directory
- [ ] Install uv package manager
- [ ] Copy project files
- [ ] Install dependencies using uv
- [ ] Expose Streamlit port (8501)
- [ ] Set command to run Streamlit app
- [ ] Configure for development mode (hot reload)

#### 1.5 Create docker-compose.yml
- [ ] Define app service
- [ ] Mount source code as volume for hot reload
- [ ] Mount data directory for database persistence
- [ ] Set up port mapping (8501:8501)
- [ ] Configure environment variables for debug mode
- [ ] Set up restart policy
- [ ] Add healthcheck (optional)

#### 1.6 Create .dockerignore
- [ ] Exclude unnecessary files from Docker build
- [ ] Exclude virtual environments
- [ ] Exclude cache directories
- [ ] Exclude git files (optional)

#### 1.7 Create data Directory
- [ ] Create `data/` directory
- [ ] Add `.gitkeep` file to preserve directory in git
- [ ] Verify `.gitignore` excludes database files

#### 1.8 Test Docker Setup
- [ ] Build Docker image
- [ ] Run container using docker-compose
- [ ] Verify Streamlit app is accessible
- [ ] Verify hot reload works (edit app.py, see changes)
- [ ] Verify logger outputs correctly
- [ ] Test stopping and restarting container

### Acceptance Criteria
- ✅ Docker container builds successfully
- ✅ Streamlit app runs and displays hello world
- ✅ Logger module works and outputs logs
- ✅ Hot reload works when editing files
- ✅ App accessible at http://localhost:8501
- ✅ Debug mode enabled for local development

---

## Task 2: Database Setup with SQLModel

### Objectives
- Set up SQLModel ORM
- Create database connection and session management
- Initialize database schema

### Subtasks

#### 2.1 Add SQLModel Dependency
- [ ] Add `sqlmodel>=0.0.14` to `pyproject.toml` dependencies

#### 2.2 Create Database Module (`src/vibe_todo/database.py`)
- [ ] Import SQLModel, create_engine, Session
- [ ] Create `get_engine()` function with singleton pattern
- [ ] Configure SQLite connection string: `sqlite:///data/todos.db`
- [ ] Create `get_session()` context manager/generator
- [ ] Create `create_db_and_tables()` function
- [ ] Add error handling for database operations
- [ ] Integrate logger for database operations

#### 2.3 Initialize Database in App
- [ ] Call `create_db_and_tables()` on app startup
- [ ] Add error handling for initialization
- [ ] Log database initialization status

### Acceptance Criteria
- ✅ SQLModel dependency installed
- ✅ Database engine created successfully
- ✅ Database file created in `data/` directory
- ✅ Session management works correctly
- ✅ Database operations logged

---

## Task 3: Create SQLModel Data Models

### Objectives
- Define all database models using SQLModel
- Set up relationships between models
- Add proper field constraints and indexes

### Subtasks

#### 3.1 Create Models Module (`src/vibe_todo/models.py`)
- [ ] Import necessary SQLModel components
- [ ] Import datetime and date types
- [ ] Create `List` model with all fields and relationships
- [ ] Create `Task` model with all fields and relationships
- [ ] Create `Subtask` model with all fields and relationships
- [ ] Create `MyDayTask` model (many-to-many) with all fields
- [ ] Add proper type hints throughout
- [ ] Add field constraints (unique, index, foreign keys)
- [ ] Configure relationship back_populates

#### 3.2 Update Database Module
- [ ] Import all models in `database.py` to register them
- [ ] Ensure models are imported before `create_db_and_tables()`

#### 3.3 Test Model Creation
- [ ] Run app to create tables
- [ ] Verify tables created in database
- [ ] Check table schemas match models

### Acceptance Criteria
- ✅ All models defined with proper structure
- ✅ Relationships configured correctly
- ✅ Database tables created successfully
- ✅ Foreign key constraints working
- ✅ Models can be imported without errors

---

## Task 4: Implement List Services

### Objectives
- Create service functions for list CRUD operations
- Handle system lists initialization
- Add proper error handling and logging

### Subtasks

#### 4.1 Create Services Module Structure (`src/vibe_todo/services.py`)
- [ ] Import SQLModel Session and select
- [ ] Import all models
- [ ] Import logger
- [ ] Create helper functions section

#### 4.2 Implement List Service Functions
- [ ] `create_list(name: str, session: Session) -> List`
- [ ] `get_all_lists(session: Session) -> List[List]`
- [ ] `get_list_by_id(list_id: int, session: Session) -> List | None`
- [ ] `update_list(list_id: int, name: str, session: Session) -> List`
- [ ] `delete_list(list_id: int, session: Session) -> bool`
- [ ] `get_system_lists(session: Session) -> List[List]`
- [ ] `get_or_create_system_list(name: str, session: Session) -> List`

#### 4.3 Add System Lists Initialization
- [ ] Create function to seed default system lists
- [ ] Lists: "My Day", "Important", "Planned", "Tasks"
- [ ] Call initialization in database setup
- [ ] Handle duplicate prevention

#### 4.4 Add Error Handling
- [ ] Handle unique constraint violations
- [ ] Handle foreign key violations
- [ ] Add logging for errors
- [ ] Return appropriate error responses

### Acceptance Criteria
- ✅ All list service functions implemented
- ✅ System lists created on initialization
- ✅ Error handling works correctly
- ✅ Functions properly typed with type hints
- ✅ Logging integrated

---

## Task 5: Implement Task Services

### Objectives
- Create service functions for task CRUD operations
- Implement task filtering and querying
- Handle My Day functionality

### Subtasks

#### 5.1 Implement Basic Task Service Functions
- [ ] `create_task(list_id: int, title: str, session: Session, **kwargs) -> Task`
- [ ] `get_task_by_id(task_id: int, session: Session) -> Task | None`
- [ ] `get_tasks_by_list(list_id: int, session: Session) -> List[Task]`
- [ ] `update_task(task_id: int, session: Session, **kwargs) -> Task`
- [ ] `delete_task(task_id: int, session: Session) -> bool`

#### 5.2 Implement Task Status Functions
- [ ] `toggle_complete(task_id: int, session: Session) -> Task`
- [ ] `toggle_important(task_id: int, session: Session) -> Task`

#### 5.3 Implement Task Query Functions
- [ ] `get_important_tasks(session: Session) -> List[Task]`
- [ ] `get_planned_tasks(session: Session) -> List[Task]`
- [ ] `get_all_tasks(session: Session, filters: dict | None = None) -> List[Task]`

#### 5.4 Implement My Day Functions
- [ ] `get_my_day_tasks(date: date, session: Session) -> List[Task]`
- [ ] `add_to_my_day(task_id: int, date: date, session: Session) -> MyDayTask`
- [ ] `remove_from_my_day(task_id: int, date: date, session: Session) -> bool`

#### 5.5 Add Error Handling and Logging
- [ ] Handle invalid task IDs
- [ ] Handle invalid list IDs
- [ ] Add logging for all operations
- [ ] Handle transaction rollbacks

### Acceptance Criteria
- ✅ All task service functions implemented
- ✅ Task queries work correctly
- ✅ My Day functionality works
- ✅ Error handling comprehensive
- ✅ Proper type hints throughout

---

## Task 6: Implement Subtask Services

### Objectives
- Create service functions for subtask operations
- Link subtasks to parent tasks

### Subtasks

#### 6.1 Implement Subtask Service Functions
- [ ] `create_subtask(task_id: int, title: str, session: Session) -> Subtask`
- [ ] `get_subtasks_by_task(task_id: int, session: Session) -> List[Subtask]`
- [ ] `toggle_subtask_complete(subtask_id: int, session: Session) -> Subtask`
- [ ] `delete_subtask(subtask_id: int, session: Session) -> bool`

#### 6.2 Add Error Handling
- [ ] Handle invalid task IDs
- [ ] Handle invalid subtask IDs
- [ ] Add logging

### Acceptance Criteria
- ✅ All subtask functions implemented
- ✅ Subtasks properly linked to tasks
- ✅ Error handling works

---

## Task 7: Create Streamlit UI Foundation

### Objectives
- Set up Streamlit app structure
- Create navigation sidebar
- Implement session state management
- Integrate database engine caching

### Subtasks

#### 7.1 Set Up App Structure (`app.py`)
- [ ] Import Streamlit and necessary modules
- [ ] Import database and service modules
- [ ] Import logger
- [ ] Set page config (title, layout, etc.)
- [ ] Create cached database engine function using `st.cache_resource`

#### 7.2 Create Navigation Sidebar
- [ ] Create sidebar with navigation options
- [ ] Add buttons/selectbox for views:
  - My Day
  - Important
  - Planned
  - Tasks (All)
  - Custom Lists (dynamic)
- [ ] Add "Add New List" button
- [ ] Store selected view in session state

#### 7.3 Implement Session State Management
- [ ] Initialize session state variables:
  - `current_view`
  - `selected_list_id`
  - `task_filters`
  - `expanded_tasks` (set)
- [ ] Create helper functions to manage state

#### 7.4 Create Database Session Helper
- [ ] Create function to get database session
- [ ] Use context manager for session handling
- [ ] Integrate with Streamlit's execution flow

### Acceptance Criteria
- ✅ App structure set up correctly
- ✅ Navigation sidebar functional
- ✅ Session state management working
- ✅ Database engine cached properly
- ✅ Database sessions handled correctly

---

## Task 8: Implement My Day View

### Objectives
- Create My Day view UI
- Display tasks added to today's My Day
- Allow adding/removing tasks from My Day

### Subtasks

#### 8.1 Create My Day View Function
- [ ] Create `render_my_day_view()` function
- [ ] Get today's date
- [ ] Fetch My Day tasks using service
- [ ] Display empty state if no tasks

#### 8.2 Create Task Card Component
- [ ] Create reusable `render_task_card()` function
- [ ] Display task title, description, due date
- [ ] Add completion checkbox
- [ ] Add important flag indicator
- [ ] Add "Remove from My Day" button
- [ ] Add edit/delete buttons

#### 8.3 Implement Task Actions
- [ ] Handle task completion toggle
- [ ] Handle important toggle
- [ ] Handle remove from My Day
- [ ] Handle task deletion
- [ ] Add confirmation for deletions

#### 8.4 Add Task to My Day Functionality
- [ ] Create "Add Task to My Day" section
- [ ] Show list of available tasks
- [ ] Allow selecting and adding tasks
- [ ] Refresh view after adding

### Acceptance Criteria
- ✅ My Day view displays correctly
- ✅ Tasks can be added/removed from My Day
- ✅ Task actions work (complete, important, delete)
- ✅ Empty state shown when no tasks
- ✅ UI updates after actions

---

## Task 9: Implement Important View

### Objectives
- Create Important view UI
- Display all important tasks
- Allow filtering by completion status

### Subtasks

#### 9.1 Create Important View Function
- [ ] Create `render_important_view()` function
- [ ] Fetch important tasks using service
- [ ] Add filter for completion status (all/completed/incomplete)
- [ ] Display filtered tasks

#### 9.2 Implement Filtering
- [ ] Add filter selectbox in sidebar or view
- [ ] Filter tasks based on selection
- [ ] Update session state with filter

#### 9.3 Reuse Task Card Component
- [ ] Use existing `render_task_card()` function
- [ ] Ensure all task actions work

### Acceptance Criteria
- ✅ Important view displays all important tasks
- ✅ Filtering works correctly
- ✅ Task actions functional
- ✅ Empty state handled

---

## Task 10: Implement Planned View

### Objectives
- Create Planned view UI
- Display tasks with due dates
- Group tasks by date (Today, Tomorrow, This Week, Later)

### Subtasks

#### 10.1 Create Planned View Function
- [ ] Create `render_planned_view()` function
- [ ] Fetch planned tasks using service
- [ ] Group tasks by date categories

#### 10.2 Implement Date Grouping Logic
- [ ] Create helper function to categorize dates
- [ ] Categories: Today, Tomorrow, This Week, Later
- [ ] Sort tasks within each category

#### 10.3 Display Grouped Tasks
- [ ] Create sections for each date category
- [ ] Display tasks under appropriate section
- [ ] Show date headers
- [ ] Handle tasks without due dates (optional)

### Acceptance Criteria
- ✅ Planned view displays tasks grouped by date
- ✅ Date grouping logic correct
- ✅ Tasks sorted properly
- ✅ Empty states handled

---

## Task 11: Implement Tasks View (All Tasks)

### Objectives
- Create view showing all tasks
- Implement filtering and search functionality

### Subtasks

#### 11.1 Create Tasks View Function
- [ ] Create `render_tasks_view()` function
- [ ] Fetch all tasks using service
- [ ] Display tasks with filters

#### 11.2 Implement Filtering
- [ ] Add filter by list (selectbox)
- [ ] Add filter by completion status
- [ ] Add filter by important flag
- [ ] Combine filters in query

#### 11.3 Implement Search
- [ ] Add search input field
- [ ] Filter tasks by title/description matching search
- [ ] Update results in real-time

#### 11.4 Display Results
- [ ] Show filtered/search results
- [ ] Display task count
- [ ] Show empty state when no results

### Acceptance Criteria
- ✅ Tasks view shows all tasks
- ✅ Filtering works correctly
- ✅ Search functionality works
- ✅ Results update properly

---

## Task 12: Implement List Management UI

### Objectives
- Create UI for managing custom lists
- Allow creating, editing, deleting lists
- Display tasks within lists

### Subtasks

#### 12.1 Create List View Function
- [ ] Create `render_list_view(list_id: int)` function
- [ ] Fetch list and its tasks
- [ ] Display list name and tasks

#### 12.2 Implement Create List Functionality
- [ ] Create form/modal for new list
- [ ] Input field for list name
- [ ] Submit button
- [ ] Handle creation and refresh

#### 12.3 Implement Edit List Functionality
- [ ] Add edit button for lists
- [ ] Create edit form
- [ ] Update list name
- [ ] Handle errors (duplicate names)

#### 12.4 Implement Delete List Functionality
- [ ] Add delete button
- [ ] Show confirmation dialog
- [ ] Handle deletion
- [ ] Handle lists with tasks (prevent or cascade)

#### 12.5 Display List Tasks
- [ ] Show tasks in selected list
- [ ] Allow creating tasks in list
- [ ] Use task card component

### Acceptance Criteria
- ✅ Lists can be created, edited, deleted
- ✅ List view displays correctly
- ✅ Tasks can be created in lists
- ✅ Error handling works

---

## Task 13: Implement Task Creation/Editing UI

### Objectives
- Create forms for creating and editing tasks
- Handle all task properties
- Integrate with My Day functionality

### Subtasks

#### 13.1 Create Task Form Component
- [ ] Create `render_task_form()` function
- [ ] Add input fields:
  - Title (required)
  - Description (textarea)
  - List selector (dropdown)
  - Due date picker
  - Important checkbox
  - Add to My Day checkbox
- [ ] Add submit/cancel buttons

#### 13.2 Implement Create Task Flow
- [ ] Show form in modal or expandable section
- [ ] Handle form submission
- [ ] Validate required fields
- [ ] Create task using service
- [ ] Add to My Day if checked
- [ ] Refresh view

#### 13.3 Implement Edit Task Flow
- [ ] Pre-populate form with task data
- [ ] Handle form submission
- [ ] Update task using service
- [ ] Handle My Day updates
- [ ] Refresh view

#### 13.4 Add Subtask Creation
- [ ] Add subtask input in task form/card
- [ ] Allow adding multiple subtasks
- [ ] Display existing subtasks
- [ ] Handle subtask completion

### Acceptance Criteria
- ✅ Task creation form works
- ✅ Task editing works
- ✅ All task properties handled
- ✅ Subtasks can be added
- ✅ Form validation works

---

## Task 14: UI/UX Enhancements

### Objectives
- Improve app appearance and user experience
- Add styling, loading states, and feedback

### Subtasks

#### 14.1 Add Custom Styling
- [ ] Create custom CSS file or use Streamlit's theming
- [ ] Style task cards
- [ ] Improve sidebar appearance
- [ ] Add color scheme

#### 14.2 Add Loading States
- [ ] Show loading indicators during operations
- [ ] Use `st.spinner()` for long operations
- [ ] Disable buttons during operations

#### 14.3 Add User Feedback
- [ ] Show success messages after operations
- [ ] Show error messages for failures
- [ ] Use `st.success()`, `st.error()`, `st.warning()`
- [ ] Add toast notifications (if using streamlit-toast)

#### 14.4 Improve Empty States
- [ ] Create attractive empty state messages
- [ ] Add icons or illustrations
- [ ] Provide action buttons in empty states

#### 14.5 Add Icons
- [ ] Use emojis or icon library
- [ ] Add icons to navigation items
- [ ] Add icons to action buttons
- [ ] Add icons to task status indicators

### Acceptance Criteria
- ✅ App looks polished and professional
- ✅ Loading states work correctly
- ✅ User feedback clear and helpful
- ✅ Empty states informative
- ✅ Icons enhance UX

---

## Task 15: Testing

### Objectives
- Write unit tests for services
- Write integration tests for database operations
- Test Streamlit app flows

### Subtasks

#### 15.1 Set Up Test Infrastructure
- [ ] Configure pytest for testing
- [ ] Create test database setup (in-memory SQLite)
- [ ] Create test fixtures for database sessions
- [ ] Create test fixtures for sample data

#### 15.2 Write Model Tests
- [ ] Test model creation
- [ ] Test model validation
- [ ] Test relationships

#### 15.3 Write Service Tests
- [ ] Test list service functions
- [ ] Test task service functions
- [ ] Test subtask service functions
- [ ] Test error handling

#### 15.4 Write Integration Tests
- [ ] Test database operations end-to-end
- [ ] Test service interactions
- [ ] Test data persistence

#### 15.5 Write UI Tests (Optional)
- [ ] Test Streamlit app initialization
- [ ] Test view rendering (if possible)
- [ ] Test user interactions (if possible)

### Acceptance Criteria
- ✅ Test suite runs successfully
- ✅ Good test coverage for services
- ✅ Tests are maintainable
- ✅ CI/CD can run tests

---

## Task 16: Documentation & Final Polish

### Objectives
- Complete documentation
- Add error handling throughout
- Final code review and cleanup

### Subtasks

#### 16.1 Update README.md
- [ ] Add project description
- [ ] Add installation instructions
- [ ] Add Docker setup instructions
- [ ] Add usage guide
- [ ] Add features list
- [ ] Add development guide
- [ ] Add screenshots (optional)

#### 16.2 Add Code Documentation
- [ ] Add docstrings to all functions
- [ ] Add module-level docstrings
- [ ] Document complex logic
- [ ] Add type hints where missing

#### 16.3 Final Error Handling Review
- [ ] Review all error handling
- [ ] Add missing error handling
- [ ] Improve error messages
- [ ] Add logging for errors

#### 16.4 Code Cleanup
- [ ] Remove unused imports
- [ ] Remove commented code
- [ ] Fix linting issues
- [ ] Format code consistently

#### 16.5 Final Testing
- [ ] Test all features end-to-end
- [ ] Test error scenarios
- [ ] Test edge cases
- [ ] Verify Docker setup works

### Acceptance Criteria
- ✅ Documentation complete
- ✅ Code well-documented
- ✅ Error handling comprehensive
- ✅ Code clean and linted
- ✅ All features working

---

## Notes

- Tasks should be completed in order
- Each task builds on previous tasks
- Test after completing each task
- Commit after each completed task
- Update this document as tasks are completed
