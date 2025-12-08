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
- [ ] Support cross-platform builds (works with Colima auto-detection)

### 3.2 Create docker-compose.yml
- [ ] Define app service
- [ ] Mount source code as volume for hot reload
- [ ] Mount data directory for database persistence
- [ ] Set up port mapping (8501:8501)
- [ ] Configure environment variables for debug mode
- [ ] Set up restart policy
- [ ] Add healthcheck (optional)
- [ ] Configure for cross-platform compatibility (Mac/Colima and Linux)
- [ ] Allow platform auto-detection (Colima handles this automatically)

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
- ✅ Works on Mac with Colima (both Intel and Apple Silicon)
- ✅ Works on Linux (x86_64)
- ✅ Platform architecture handled correctly

## Colima Setup (Mac)
1. Install Colima: `brew install colima`
2. Start Colima: `colima start`
3. Verify Docker is working: `docker ps`
4. Build and run: `docker compose up --build`

## Platform Notes
- **Mac with Colima**: Automatically detects and uses correct platform (arm64 for Apple Silicon, amd64 for Intel)
- **Linux**: Uses native platform (typically amd64)
- **Manual override**: Set `DOCKER_DEFAULT_PLATFORM=linux/amd64` environment variable to force amd64 builds

## Notes
- Use `--reload` flag or similar for Streamlit hot reload
- Volume mounts should include `src/` and `app.py`
- Data directory should persist between container restarts
- **Cross-platform compatibility**: Docker configuration should work on both Mac (with Colima) and Linux
- **Colima on Mac**: Colima automatically handles platform detection (arm64 for Apple Silicon, amd64 for Intel)
- **Platform detection**: Docker will auto-detect the correct platform based on the host system
- **Manual platform override**: If needed, you can specify platform in docker-compose.yml:
  - `platform: linux/amd64` for Intel Mac or Linux x86_64
  - `platform: linux/arm64` for Apple Silicon Mac
- **Colima setup**: Ensure Colima is running (`colima start`) before building/running containers
- For consistent builds across teams, consider using `linux/amd64` as default (works on both via emulation)
