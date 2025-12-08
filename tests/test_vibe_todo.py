"""Placeholder tests for vibe-todo package."""

from vibe_todo import hello


def test_hello():
    """Test that hello function returns expected string."""
    result = hello()
    assert isinstance(result, str)
    assert result == "Hello from vibe-todo!"
