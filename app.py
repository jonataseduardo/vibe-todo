"""Streamlit application entry point for vibe-todo."""

import streamlit as st
from sqlalchemy import Engine

from vibe_todo.database import create_db_and_tables, get_engine, get_session
from vibe_todo.logger import logger
from vibe_todo.services import get_all_lists

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
if "selected_view" not in st.session_state:
    st.session_state.selected_view = "My Day"
if "show_add_list_dialog" not in st.session_state:
    st.session_state.show_add_list_dialog = False

# create navigation sidebar
with st.sidebar:
    st.title("📋 Vibe Todo")
    st.divider()
    
    # System views
    st.subheader("Views")
    
    # My Day button
    if st.button("📅 My Day", use_container_width=True, type="primary" if st.session_state.selected_view == "My Day" else "secondary"):
        st.session_state.selected_view = "My Day"
        st.rerun()
    
    # Important button
    if st.button("⭐ Important", use_container_width=True, type="primary" if st.session_state.selected_view == "Important" else "secondary"):
        st.session_state.selected_view = "Important"
        st.rerun()
    
    # Planned button
    if st.button("📆 Planned", use_container_width=True, type="primary" if st.session_state.selected_view == "Planned" else "secondary"):
        st.session_state.selected_view = "Planned"
        st.rerun()
    
    # Tasks (All) button
    if st.button("📝 Tasks", use_container_width=True, type="primary" if st.session_state.selected_view == "Tasks" else "secondary"):
        st.session_state.selected_view = "Tasks"
        st.rerun()
    
    st.divider()
    
    # Custom Lists section
    st.subheader("Lists")
    
    # Fetch custom lists (non-system lists)
    try:
        with get_session() as session:
            all_lists = get_all_lists(session)
            custom_lists = [lst for lst in all_lists if not lst.is_system]
            
            # Display custom lists
            for custom_list in custom_lists:
                if st.button(
                    f"📁 {custom_list.name}",
                    use_container_width=True,
                    type="primary" if st.session_state.selected_view == f"List:{custom_list.id}" else "secondary",
                    key=f"list_{custom_list.id}"
                ):
                    st.session_state.selected_view = f"List:{custom_list.id}"
                    st.rerun()
    except Exception as e:
        logger.error(f"Failed to fetch custom lists: {e}")
        st.error("Failed to load custom lists")
    
    st.divider()
    
    # Add New List button
    if st.button("➕ Add New List", use_container_width=True, type="secondary"):
        st.session_state.show_add_list_dialog = True
        st.rerun()

# Handle Add New List dialog
if st.session_state.show_add_list_dialog:
    with st.sidebar:
        st.divider()
        st.subheader("Add New List")
        new_list_name = st.text_input("List name", placeholder="Enter list name", key="new_list_name_input")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Create", use_container_width=True):
                if new_list_name and new_list_name.strip():
                    try:
                        from vibe_todo.services import create_list
                        with get_session() as session:
                            new_list = create_list(new_list_name.strip(), session)
                            logger.info(f"Created new list: {new_list.name}")
                            st.success(f"List '{new_list.name}' created!")
                            st.session_state.show_add_list_dialog = False
                            st.session_state.selected_view = f"List:{new_list.id}"
                            st.rerun()
                    except Exception as e:
                        logger.error(f"Failed to create list: {e}")
                        st.error(f"Failed to create list: {e}")
                else:
                    st.warning("Please enter a list name")
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_add_list_dialog = False
                st.rerun()

# main content
st.title("Hello World!")
st.header("Welcome to Vibe Todo")
st.write("This is a Microsoft TODO-like application built with Streamlit.")
st.write(f"**Current view:** {st.session_state.selected_view}")

# log that page was rendered
logger.info("Hello world page rendered successfully")
