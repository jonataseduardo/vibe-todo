# Task 6: Create SQLModel Data Models - Part 1

## Objectives
- Define database models using SQLModel
- Set up List and Task models
- Configure relationships

## Subtasks

### 6.1 Create Models Module Structure (`src/vibe_todo/models.py`)
- [ ] Import necessary SQLModel components
- [ ] Import datetime and date types
- [ ] Create `List` model with all fields and relationships

### 6.2 Create Task Model
- [ ] Create `Task` model with all fields and relationships
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

## Notes
- Models should use SQLModel with `table=True`
- Use `Field()` for constraints and defaults
- Relationships use `Relationship()` with `back_populates`
