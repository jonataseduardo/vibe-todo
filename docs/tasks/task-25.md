# Task 25: Implement Task Creation/Editing UI - Part 1

## Objectives
- Create task form component
- Implement create task flow

## Subtasks

### 25.1 Create Task Form Component
- [ ] Create `render_task_form()` function
- [ ] Add input fields:
  - Title (required)
  - Description (textarea)
  - List selector (dropdown)
  - Due date picker
  - Important checkbox
  - Add to My Day checkbox
- [ ] Add submit/cancel buttons

### 25.2 Implement Create Task Flow
- [ ] Show form in modal or expandable section
- [ ] Handle form submission
- [ ] Validate required fields
- [ ] Create task using service
- [ ] Add to My Day if checked
- [ ] Refresh view

## Acceptance Criteria
- ✅ Task creation form works
- ✅ All task properties handled
- ✅ Form validation works
- ✅ Tasks created successfully

## Notes
- Use Streamlit form for submission
- Validate title is not empty
- Show success message after creation
