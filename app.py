"""Streamlit application entry point for vibe-todo."""

import streamlit as st

from vibe_todo.database import create_db_and_tables
from vibe_todo.logger import logger

# configure page
st.set_page_config(
    page_title="Vibe Todo",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# initialize logger
logger.info("Application started")

# initialize database
try:
    create_db_and_tables()
    logger.info("Database initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database: {e}")
    st.error("Failed to initialize database. Please check the logs.")
    st.stop()

# main content
st.title("Hello World!")
st.header("Welcome to Vibe Todo")
st.write("This is a Microsoft TODO-like application built with Streamlit.")

# log that page was rendered
logger.info("Hello world page rendered successfully")
