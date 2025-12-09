from contextlib import contextmanager
from typing import Generator
import streamlit as st
from sqlmodel import Session
from vibe_todo.database import get_session as _get_session
from vibe_todo.logger import logger

@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Streamlit-aware database session context manager.
    Handles errors by showing a Streamlit error message.
    """
    try:
        with _get_session() as session:
            yield session
    except Exception as e:
        logger.error(f"Database error: {e}")
        st.error(f"An error occurred: {e}")
        raise e
