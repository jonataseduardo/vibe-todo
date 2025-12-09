"""UI components for vibe-todo application."""

from datetime import date, timedelta
import streamlit as st
from sqlmodel import Session

from vibe_todo.models import Task
from vibe_todo.services import (
    toggle_complete,
    toggle_important,
    remove_from_my_day,
    delete_task,
    get_my_day_tasks,
    get_all_tasks,
    add_to_my_day,
    get_important_tasks,
    get_planned_tasks
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

                if st.session_state.get(f"confirm_delete_{task.id}"):
                    st.warning("Are you sure?")
                    col_del_1, col_del_2 = st.columns(2)
                    with col_del_1:
                        if st.button("Yes", key=f"confirm_del_btn_{task.id}", type="primary", use_container_width=True):
                            on_delete()
                    with col_del_2:
                        if st.button("No", key=f"cancel_del_btn_{task.id}", use_container_width=True):
                            st.session_state[f"confirm_delete_{task.id}"] = False
                            st.rerun()
                else:
                    if st.button("🗑️ Delete", key=f"delete_{task.id}", type="primary", use_container_width=True):
                        st.session_state[f"confirm_delete_{task.id}"] = True
                        st.rerun()


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
        else:
            for task in tasks:
                render_task_card(task, session, show_remove_from_my_day=True)

        st.divider()
        with st.expander("➕ Add tasks from other lists"):
            all_tasks = get_all_tasks(session)
            # Filter out tasks already in My Day and completed tasks
            my_day_ids = {t.id for t in tasks} if tasks else set()
            available_tasks = [t for t in all_tasks if t.id not in my_day_ids and not t.is_completed]
            
            if not available_tasks:
                st.info("No available tasks to add.")
            else:
                for task in available_tasks:
                    c1, c2 = st.columns([0.8, 0.2])
                    with c1:
                        st.write(f"{task.title}")
                    with c2:
                        if st.button("Add", key=f"add_to_my_day_{task.id}"):
                            add_to_my_day(task.id, today, session)
                            st.rerun()
            
    except Exception as e:
        logger.error(f"Error rendering My Day view: {e}")
        st.error("Failed to load My Day tasks")


def render_important_view(session: Session):
    """
    Render the 'Important' view.

    Args:
        session: Database session
    """
    st.title("⭐ Important")
    
    # Filter controls
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        filter_status = st.selectbox(
            "Filter by status",
            ["All", "Incomplete", "Completed"],
            key="important_filter_status",
            label_visibility="collapsed"
        )

    try:
        tasks = get_important_tasks(session)
        
        # Apply filters
        if filter_status == "Incomplete":
            tasks = [t for t in tasks if not t.is_completed]
        elif filter_status == "Completed":
            tasks = [t for t in tasks if t.is_completed]
            
        st.caption(f"{len(tasks)} tasks")
        
        if not tasks:
            if filter_status == "All":
                st.info("No important tasks found. Mark tasks as important to see them here!")
            else:
                st.info(f"No {filter_status.lower()} important tasks found.")
        else:
            for task in tasks:
                render_task_card(task, session)

    except Exception as e:
        logger.error(f"Error rendering Important view: {e}")
        st.error("Failed to load Important tasks")


def _group_tasks_by_date(tasks: list[Task]) -> dict[str, list[Task]]:
    """
    Helper function to group tasks by date categories.
    
    Categories:
    - Today: due_date <= today
    - Tomorrow: due_date == tomorrow
    - This Week: tomorrow < due_date <= today + 7 days
    - Later: due_date > today + 7 days
    """
    grouped = {
        "Today": [],
        "Tomorrow": [],
        "This Week": [],
        "Later": []
    }
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    next_week_end = today + timedelta(days=7)
    
    for task in tasks:
        if not task.due_date:
            continue
            
        d = task.due_date
        
        if d <= today:
            grouped["Today"].append(task)
        elif d == tomorrow:
            grouped["Tomorrow"].append(task)
        elif tomorrow < d <= next_week_end:
            grouped["This Week"].append(task)
        else:
            grouped["Later"].append(task)
            
    return grouped


def render_planned_view(session: Session):
    """
    Render the 'Planned' view.

    Args:
        session: Database session
    """
    st.title("📆 Planned")

    try:
        tasks = get_planned_tasks(session)
        
        # Sort by due date
        tasks.sort(key=lambda t: t.due_date if t.due_date else date.max)
        
        # Group tasks
        grouped = _group_tasks_by_date(tasks)
        
        # Check if we have any tasks
        if not tasks:
            st.info("No planned tasks found. Add a due date to your tasks to see them here!")
            return

        # Render groups
        # Today
        if grouped["Today"]:
            with st.expander(f"Today ({len(grouped['Today'])})", expanded=True):
                for task in grouped["Today"]:
                    render_task_card(task, session)
        
        # Tomorrow
        if grouped["Tomorrow"]:
            with st.expander(f"Tomorrow ({len(grouped['Tomorrow'])})", expanded=True):
                for task in grouped["Tomorrow"]:
                    render_task_card(task, session)

        # This Week
        if grouped["This Week"]:
            with st.expander(f"This Week ({len(grouped['This Week'])})", expanded=True):
                for task in grouped["This Week"]:
                    render_task_card(task, session)
                    
        # Later
        if grouped["Later"]:
            with st.expander(f"Later ({len(grouped['Later'])})", expanded=False):
                for task in grouped["Later"]:
                    render_task_card(task, session)
                    
        # If all groups are empty (shouldn't happen if tasks is not empty, unless due_dates are missing which is filtered)
        if not any(grouped.values()):
             st.info("No planned tasks found.")

    except Exception as e:
        logger.error(f"Error rendering Planned view: {e}")
        st.error("Failed to load Planned tasks")
