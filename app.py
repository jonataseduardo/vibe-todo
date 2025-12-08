"""Streamlit application entry point for vibe-todo."""

import streamlit as st

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

# main content
st.title("Hello World!")
st.header("Welcome to Vibe Todo")
st.write("This is a Microsoft TODO-like application built with Streamlit.")

# log that page was rendered
logger.info("Hello world page rendered successfully")
