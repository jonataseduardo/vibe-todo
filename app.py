"""Streamlit application entry point for vibe-todo."""

import streamlit as st
from sqlalchemy import Engine

from vibe_todo.database import create_db_and_tables, get_engine
from vibe_todo.db_helper import get_db_session
from vibe_todo.logger import logger
from vibe_todo.services import get_all_lists, create_list
from vibe_todo.state import (
    init_session_state,
    get_current_view,
    set_current_view,
    get_selected_list_id,
    get_show_add_list_dialog,
    set_show_add_list_dialog
)
from vibe_todo.ui import render_my_day_view

# configure page
st.set_page_config(
    page_title="Vibe Todo",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# initialize logger
logger.info("Application started")


@st.cache_resource
def get_cached_engine() -> Engine:
    """
    Get cached database engine using Streamlit's cache_resource.
    
    This ensures the engine is created once and reused across reruns.
    
    Returns:
        Engine: SQLModel engine instance
    """
    try:
        engine = get_engine()
        logger.info("Database engine cached successfully")
        return engine
    except Exception as e:
        logger.error(f"Failed to cache database engine: {e}")
        raise


# initialize database
try:
    # Use cached engine to initialize database
    engine = get_cached_engine()
    create_db_and_tables()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    st.error("Failed to initialize database. Please check the logs.")
    st.stop()

# initialize session state
init_session_state()

# create navigation sidebar
with st.sidebar:
    st.title("📋 Vibe Todo")
    st.divider()
    
    # System views
    st.subheader("Views")
    
    current_view = get_current_view()
    
    # My Day button
    if st.button("📅 My Day", use_container_width=True, type="primary" if current_view == "My Day" else "secondary"):
        set_current_view("My Day")
        st.rerun()
    
    # Important button
    if st.button("⭐ Important", use_container_width=True, type="primary" if current_view == "Important" else "secondary"):
        set_current_view("Important")
        st.rerun()
    
    # Planned button
    if st.button("📆 Planned", use_container_width=True, type="primary" if current_view == "Planned" else "secondary"):
        set_current_view("Planned")
        st.rerun()
    
    # Tasks (All) button
    if st.button("📝 Tasks", use_container_width=True, type="primary" if current_view == "Tasks" else "secondary"):
        set_current_view("Tasks")
        st.rerun()
    
    st.divider()
    
    # Custom Lists section
    st.subheader("Lists")
    
    # Fetch custom lists (non-system lists)
    try:
        with get_db_session() as session:
            all_lists = get_all_lists(session)
            custom_lists = [lst for lst in all_lists if not lst.is_system]
            
            # Display custom lists
            for custom_list in custom_lists:
                is_selected = (current_view == "List" and get_selected_list_id() == custom_list.id)
                if st.button(
                    f"📁 {custom_list.name}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary",
                    key=f"list_{custom_list.id}"
                ):
                    set_current_view("List", custom_list.id)
                    st.rerun()
    except Exception as e:
        logger.error(f"Failed to fetch custom lists: {e}")
        st.error("Failed to load custom lists")
    
    st.divider()
    
    # Add New List button
    if st.button("➕ Add New List", use_container_width=True, type="secondary"):
        set_show_add_list_dialog(True)
        st.rerun()

# Handle Add New List dialog
if get_show_add_list_dialog():
    with st.sidebar:
        st.divider()
        st.subheader("Add New List")
        new_list_name = st.text_input("List name", placeholder="Enter list name", key="new_list_name_input")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create", use_container_width=True):
                if new_list_name and new_list_name.strip():
                    try:
                        with get_db_session() as session:
                            new_list = create_list(new_list_name.strip(), session)
                            logger.info(f"Created new list: {new_list.name}")
                            st.success(f"List '{new_list.name}' created!")
                            set_show_add_list_dialog(False)
                            set_current_view("List", new_list.id)
                            st.rerun()
                    except Exception as e:
                        logger.error(f"Failed to create list: {e}")
                        st.error(f"Failed to create list: {e}")
                else:
                    st.warning("Please enter a list name")
        with col2:
            if st.button("Cancel", use_container_width=True):
                set_show_add_list_dialog(False)
                st.rerun()

# main content
current_view_name = get_current_view()
with get_db_session() as session:
    if current_view_name == "My Day":
        render_my_day_view(session)
    else:
        st.title("Hello World!")
        st.header("Welcome to Vibe Todo")
        st.write("This is a Microsoft TODO-like application built with Streamlit.")

        if current_view_name == "List":
            st.write(f"**Current view:** {current_view_name} (ID: {get_selected_list_id()})")
        else:
            st.write(f"**Current view:** {current_view_name}")

# log that page was rendered
logger.info(f"Page rendered: {current_view_name}")
