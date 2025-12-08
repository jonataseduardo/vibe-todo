# Task 3: Create Docker Configuration Files

## Objectives
- Create Dockerfile for containerized development
- Create docker-compose.yml for easy local development
- Configure hot reload and debug mode

## Subtasks

### 3.1 Create Dockerfile
- [ ] Use Python 3.13 base image
- [ ] Set working directory
- [ ] Install uv package manager
- [ ] Copy project files
- [ ] Install dependencies using uv
- [ ] Expose Streamlit port (8501)
- [ ] Set command to run Streamlit app
- [ ] Configure for development mode (hot reload)

### 3.2 Create docker-compose.yml
- [ ] Define app service
- [ ] Mount source code as volume for hot reload
- [ ] Mount data directory for database persistence
- [ ] Set up port mapping (8501:8501)
- [ ] Configure environment variables for debug mode
- [ ] Set up restart policy
- [ ] Add healthcheck (optional)

### 3.3 Create Supporting Files
- [ ] Create `.dockerignore` file
- [ ] Exclude unnecessary files from Docker build
- [ ] Create `data/` directory
- [ ] Add `.gitkeep` file to preserve directory in git

## Acceptance Criteria
- ✅ Dockerfile created and builds successfully
- ✅ docker-compose.yml configured correctly
- ✅ Hot reload works when editing files
- ✅ App accessible at http://localhost:8501
- ✅ Debug mode enabled for local development

## Notes
- Use `--reload` flag or similar for Streamlit hot reload
- Volume mounts should include `src/` and `app.py`
- Data directory should persist between container restarts
