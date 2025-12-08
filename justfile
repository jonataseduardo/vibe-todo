# Show available commands
default:
    @just --list

# Install all dependencies (dev, lint, test)
install:
    uv sync

# Run linting checks (ruff and pyright)
lint:
    uv run ruff check .
    uv run pyright

# Run tests
test:
    uv run pytest

# Run all checks (lint and test)
check: lint test
