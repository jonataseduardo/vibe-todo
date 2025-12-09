# Task 10: Implement Task Services - Part 1

## Objectives
- Implement basic task CRUD operations
- Implement task status toggle functions

## Subtasks

### 10.1 Implement Basic Task Service Functions
- [ ] `create_task(list_id: int, title: str, session: Session, **kwargs) -> Task`
- [ ] `get_task_by_id(task_id: int, session: Session) -> Task | None`
- [ ] `get_tasks_by_list(list_id: int, session: Session) -> List[Task]`

### 10.2 Implement Task Update and Delete
- [ ] `update_task(task_id: int, session: Session, **kwargs) -> Task`
- [ ] `delete_task(task_id: int, session: Session) -> bool`

### 10.3 Implement Task Status Functions
- [ ] `toggle_complete(task_id: int, session: Session) -> Task`
- [ ] `toggle_important(task_id: int, session: Session) -> Task`

## Acceptance Criteria
- ✅ Basic task CRUD functions implemented
- ✅ Task status toggle functions work
- ✅ Functions properly typed
- ✅ Error handling included

## Notes
- Toggle functions should flip the current state
- Update `updated_at` timestamp on updates
- Handle invalid IDs gracefully
