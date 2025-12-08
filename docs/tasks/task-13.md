# Task 13: Implement Subtask Services

## Objectives
- Create service functions for subtask operations
- Link subtasks to parent tasks
- Add error handling

## Subtasks

### 13.1 Implement Subtask Service Functions
- [ ] `create_subtask(task_id: int, title: str, session: Session) -> Subtask`
- [ ] `get_subtasks_by_task(task_id: int, session: Session) -> List[Subtask]`

### 13.2 Complete Subtask Functions
- [ ] `toggle_subtask_complete(subtask_id: int, session: Session) -> Subtask`
- [ ] `delete_subtask(subtask_id: int, session: Session) -> bool`

### 13.3 Add Error Handling
- [ ] Handle invalid task IDs
- [ ] Handle invalid subtask IDs
- [ ] Add logging

## Acceptance Criteria
- ✅ All subtask functions implemented
- ✅ Subtasks properly linked to tasks
- ✅ Error handling works
- ✅ Logging integrated

## Notes
- Subtasks belong to a parent task
- Deleting a task should cascade delete subtasks (or prevent deletion)
- Toggle works like task toggle
