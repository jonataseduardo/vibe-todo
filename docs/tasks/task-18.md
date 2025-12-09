# Task 18: Implement Important View

## Objectives
- Create Important view UI
- Display all important tasks
- Allow filtering by completion status

## Subtasks

### 18.1 Create Important View Function
- [ ] Create `render_important_view()` function
- [ ] Fetch important tasks using service
- [ ] Add filter for completion status (all/completed/incomplete)
- [ ] Display filtered tasks

### 18.2 Implement Filtering
- [ ] Add filter selectbox in sidebar or view
- [ ] Filter tasks based on selection
- [ ] Update session state with filter

### 18.3 Reuse Task Card Component
- [ ] Use existing `render_task_card()` function
- [ ] Ensure all task actions work

## Acceptance Criteria
- ✅ Important view displays all important tasks
- ✅ Filtering works correctly
- ✅ Task actions functional
- ✅ Empty state handled

## Notes
- Reuse task card from My Day view
- Filter should update immediately
- Show task count
