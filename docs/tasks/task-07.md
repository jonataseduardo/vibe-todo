# Task 7: Create SQLModel Data Models - Part 2

## Objectives
- Complete remaining models (Subtask, MyDayTask)
- Register models in database module
- Test model creation

## Subtasks

### 7.1 Create Remaining Models
- [ ] Create `Subtask` model with all fields and relationships
- [ ] Create `MyDayTask` model (many-to-many) with all fields
- [ ] Add proper type hints throughout
- [ ] Add field constraints (unique, index, foreign keys)

### 7.2 Update Database Module and Test
- [ ] Import all models in `database.py` to register them
- [ ] Ensure models are imported before `create_db_and_tables()`
- [ ] Run app to create tables
- [ ] Verify tables created in database
- [ ] Check table schemas match models

## Acceptance Criteria
- ✅ All models defined with proper structure
- ✅ Relationships configured correctly
- ✅ Database tables created successfully
- ✅ Foreign key constraints working
- ✅ Models can be imported without errors

## Notes
- MyDayTask uses composite primary key (task_id, date)
- All relationships should have proper back_populates
- Test that foreign keys work correctly
