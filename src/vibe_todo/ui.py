"""UI components for vibe-todo application."""

from datetime import date
import streamlit as st
from sqlmodel import Session

from vibe_todo.models import Task
from vibe_todo.services import (
    toggle_complete,
    toggle_important,
    remove_from_my_day,
    delete_task,
    get_my_day_tasks
)
from vibe_todo.logger import logger

def render_task_card(task: Task, session: Session, show_remove_from_my_day: bool = False):
    """
    Render a single task card.

    Args:
        task: The task to display
        session: Database session
        show_remove_from_my_day: Whether to show the 'Remove from My Day' button
    """
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([0.05, 0.75, 0.1, 0.1])

        with col1:
            # Completion checkbox
            # We use a callback to handle the state change immediately
            def on_complete_change():
                try:
                    toggle_complete(task.id, session)
                except Exception as e:
                    st.error(f"Error updating task: {e}")

            st.checkbox(
                "Complete",
                value=task.is_completed,
                key=f"complete_{task.id}",
                label_visibility="collapsed",
                on_change=on_complete_change
            )

        with col2:
            # Title and details
            st.markdown(f"**{task.title}**")
            details = []
            if task.description:
                details.append(task.description)
            if task.due_date:
                details.append(f"📅 {task.due_date.strftime('%Y-%m-%d')}")
            
            if details:
                st.caption(" • ".join(details))

        with col3:
            # Important toggle
            def on_important_click():
                try:
                    toggle_important(task.id, session)
                except Exception as e:
                    st.error(f"Error updating task: {e}")

            if st.button(
                "⭐" if task.is_important else "☆",
                key=f"important_{task.id}",
                help="Toggle importance",
                on_click=on_important_click
            ):
                pass

        with col4:
            # More actions (Delete, Remove from My Day)
            with st.popover("⋮"):
                if show_remove_from_my_day:
                    def on_remove_my_day():
                        try:
                            remove_from_my_day(task.id, date.today(), session)
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error removing from My Day: {e}")
                            
                    if st.button("Remove from My Day", key=f"rm_my_day_{task.id}", use_container_width=True):
                         on_remove_my_day()

                def on_delete():
                    try:
                        delete_task(task.id, session)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error deleting task: {e}")

                if st.button("🗑️ Delete", key=f"delete_{task.id}", type="primary", use_container_width=True):
                    on_delete()


def render_my_day_view(session: Session):
    """
    Render the 'My Day' view.

    Args:
        session: Database session
    """
    today = date.today()
    st.title(f"My Day - {today.strftime('%A, %B %d')}")
    
    try:
        tasks = get_my_day_tasks(today, session)
        
        if not tasks:
            st.info("No tasks in My Day. Add some tasks from other lists!")
            return

        for task in tasks:
            render_task_card(task, session, show_remove_from_my_day=True)
            
    except Exception as e:
        logger.error(f"Error rendering My Day view: {e}")
        st.error("Failed to load My Day tasks")
