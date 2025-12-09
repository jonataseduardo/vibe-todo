# Task 15: Create Streamlit UI Foundation - Part 2

## Objectives
- Implement session state management
- Create database session helper

## Subtasks

### 15.1 Implement Session State Management
- [x] Initialize session state variables:
  - `current_view`
  - `selected_list_id`
  - `task_filters`
  - `expanded_tasks` (set)
- [x] Create helper functions to manage state

### 15.2 Create Database Session Helper
- [x] Create function to get database session
- [x] Use context manager for session handling
- [x] Integrate with Streamlit's execution flow

## Acceptance Criteria
- ✅ Session state management working
- ✅ Database sessions handled correctly
- ✅ Helper functions created
- ✅ State persists across interactions

## Notes
- Session state should initialize with defaults
- Database sessions should be created per operation
- Use context managers for proper cleanup
