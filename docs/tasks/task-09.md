# Task 9: Implement List Services - Part 2

## Objectives
- Complete list service functions
- Add system lists initialization
- Add error handling

## Subtasks

### 9.1 Complete List Service Functions
- [ ] `update_list(list_id: int, name: str, session: Session) -> List`
- [ ] `delete_list(list_id: int, session: Session) -> bool`
- [ ] `get_system_lists(session: Session) -> List[List]`
- [ ] `get_or_create_system_list(name: str, session: Session) -> List`

### 9.2 Add System Lists Initialization
- [ ] Create function to seed default system lists
- [ ] Lists: "My Day", "Important", "Planned", "Tasks"
- [ ] Call initialization in database setup
- [ ] Handle duplicate prevention

### 9.3 Add Error Handling
- [ ] Handle unique constraint violations
- [ ] Handle foreign key violations
- [ ] Add logging for errors
- [ ] Return appropriate error responses

## Acceptance Criteria
- ✅ All list service functions implemented
- ✅ System lists created on initialization
- ✅ Error handling works correctly
- ✅ Functions properly typed with type hints
- ✅ Logging integrated

## Notes
- System lists should be created automatically on first run
- Use try-except for error handling
- Log errors with appropriate level
