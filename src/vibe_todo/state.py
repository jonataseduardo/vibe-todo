import streamlit as st
from typing import Set, Dict, Optional, Any

def init_session_state():
    """Initialize session state variables if they don't exist."""
    if "current_view" not in st.session_state:
        st.session_state.current_view = "My Day"
    if "selected_list_id" not in st.session_state:
        st.session_state.selected_list_id = None
    if "task_filters" not in st.session_state:
        st.session_state.task_filters = {}
    if "expanded_tasks" not in st.session_state:
        st.session_state.expanded_tasks = set()
    if "show_add_list_dialog" not in st.session_state:
        st.session_state.show_add_list_dialog = False

def get_current_view() -> str:
    """Get the current view name."""
    return st.session_state.current_view

def set_current_view(view: str, list_id: Optional[int] = None):
    """Set the current view and optionally the selected list ID."""
    st.session_state.current_view = view
    st.session_state.selected_list_id = list_id

def get_selected_list_id() -> Optional[int]:
    """Get the ID of the currently selected list."""
    return st.session_state.selected_list_id

def toggle_task_expansion(task_id: int):
    """Toggle the expansion state of a task."""
    if task_id in st.session_state.expanded_tasks:
        st.session_state.expanded_tasks.remove(task_id)
    else:
        st.session_state.expanded_tasks.add(task_id)

def is_task_expanded(task_id: int) -> bool:
    """Check if a task is expanded."""
    return task_id in st.session_state.expanded_tasks

def set_task_filter(key: str, value: Any):
    """Set a task filter value."""
    st.session_state.task_filters[key] = value

def get_task_filter(key: str, default: Any = None) -> Any:
    """Get a task filter value."""
    return st.session_state.task_filters.get(key, default)

def clear_task_filters():
    """Clear all task filters."""
    st.session_state.task_filters = {}

def get_show_add_list_dialog() -> bool:
    """Get the show_add_list_dialog state."""
    return st.session_state.show_add_list_dialog

def set_show_add_list_dialog(show: bool):
    """Set the show_add_list_dialog state."""
    st.session_state.show_add_list_dialog = show
