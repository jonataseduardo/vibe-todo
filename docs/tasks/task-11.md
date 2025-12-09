# Task 11: Implement Task Services - Part 2

## Objectives
- Implement task query functions
- Implement My Day functionality

## Subtasks

### 11.1 Implement Task Query Functions
- [ ] `get_important_tasks(session: Session) -> List[Task]`
- [ ] `get_planned_tasks(session: Session) -> List[Task]`
- [ ] `get_all_tasks(session: Session, filters: dict | None = None) -> List[Task]`

### 11.2 Implement My Day Functions
- [ ] `get_my_day_tasks(date: date, session: Session) -> List[Task]`
- [ ] `add_to_my_day(task_id: int, date: date, session: Session) -> MyDayTask`
- [ ] `remove_from_my_day(task_id: int, date: date, session: Session) -> bool`

## Acceptance Criteria
- ✅ Task query functions implemented
- ✅ My Day functionality works
- ✅ Filters work correctly
- ✅ Proper type hints throughout

## Notes
- Planned tasks are those with due_date set
- My Day uses the MyDayTask many-to-many relationship
- Filters should support multiple conditions
