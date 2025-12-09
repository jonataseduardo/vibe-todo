# Task 1: Update Dependencies and Create Logger Module

## Objectives
- Update project dependencies
- Create logging module using loguru
- Configure logger for development and production

## Subtasks

### 1.1 Update Dependencies (`pyproject.toml`)
- [ ] Add `streamlit>=1.28.0` to dependencies
- [ ] Add `loguru>=0.7.0` to dependencies
- [ ] Add `python-dateutil>=2.8.0` to dependencies (optional but helpful)

### 1.2 Create Logger Module (`src/vibe_todo/logger.py`)
- [ ] Create logger configuration using loguru
- [ ] Set up log levels (DEBUG, INFO, WARNING, ERROR)
- [ ] Configure log format with timestamps and context

### 1.3 Complete Logger Module
- [ ] Create log file rotation (optional)
- [ ] Export logger instance for use across the app
- [ ] Add function to configure logger based on environment (dev/prod)

## Acceptance Criteria
- ✅ Dependencies updated in `pyproject.toml`
- ✅ Logger module created and functional
- ✅ Logger configured for different environments
- ✅ Logger can be imported and used throughout the app

## Notes
- Logger should be easy to use: `from vibe_todo.logger import logger`
- Consider log file location: `logs/` directory or console only for dev
- Log format should include timestamp, level, and message
