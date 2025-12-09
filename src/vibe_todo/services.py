"""Services module for business logic and database operations."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from vibe_todo.logger import logger
from vibe_todo.models import List, MyDayTask, Subtask, Task


# ============================================================================
# Helper Functions Section
# ============================================================================


def initialize_system_lists(session: Session) -> list[List]:
    """
    Initialize default system lists if they don't exist.

    Creates the following system lists:
    - "My Day"
    - "Important"
    - "Planned"
    - "Tasks"

    Args:
        session: Database session

    Returns:
        list[List]: List of all system lists (existing and newly created)
    """
    logger.info("Initializing system lists")

    system_list_names = ["My Day", "Important", "Planned", "Tasks"]
    created_lists = []

    for name in system_list_names:
        try:
            list_instance = get_or_create_system_list(name, session)
            if list_instance.id not in [l.id for l in created_lists]:
                created_lists.append(list_instance)
        except Exception as e:
            logger.error(f"Failed to initialize system list '{name}': {e}")
            # Continue with other lists even if one fails
            continue

    logger.info(f"System lists initialization complete. Total system lists: {len(created_lists)}")
    return created_lists


# ============================================================================
# List Service Functions
# ============================================================================


def create_list(name: str, session: Session) -> List:
    """
    Create a new list.

    Args:
        name: Name of the list to create
        session: Database session

    Returns:
        List: The created list instance

    Raises:
        ValueError: If list name is empty or invalid
        IntegrityError: If list name already exists (unique constraint violation)
    """
    logger.info(f"Creating list with name: {name}")

    if not name or not name.strip():
        logger.error("Cannot create list with empty name")
        raise ValueError("List name cannot be empty")

    try:
        new_list = List(name=name.strip())
        session.add(new_list)
        session.commit()
        session.refresh(new_list)

        logger.info(f"Successfully created list with id: {new_list.id}, name: {name}")
        return new_list
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to create list '{name}': unique constraint violation - {e}")
        raise ValueError(f"List with name '{name}' already exists") from e


def get_all_lists(session: Session) -> list[List]:
    """
    Get all lists from the database.

    Args:
        session: Database session

    Returns:
        list[List]: List of all List instances
    """
    logger.info("Fetching all lists")

    statement = select(List)
    lists = session.exec(statement).all()

    logger.info(f"Found {len(lists)} lists")
    return list(lists)


def get_list_by_id(list_id: int, session: Session) -> List | None:
    """
    Get a list by its ID.

    Args:
        list_id: ID of the list to retrieve
        session: Database session

    Returns:
        List | None: The List instance if found, None otherwise
    """
    logger.info(f"Fetching list with id: {list_id}")

    statement = select(List).where(List.id == list_id)
    list_instance = session.exec(statement).first()

    if list_instance:
        logger.info(f"Found list with id: {list_id}, name: {list_instance.name}")
    else:
        logger.warning(f"List with id: {list_id} not found")

    return list_instance


def update_list(list_id: int, name: str, session: Session) -> List:
    """
    Update an existing list's name.

    Args:
        list_id: ID of the list to update
        name: New name for the list
        session: Database session

    Returns:
        List: The updated list instance

    Raises:
        ValueError: If list name is empty or list not found
        IntegrityError: If list name already exists (unique constraint violation)
    """
    logger.info(f"Updating list with id: {list_id}, new name: {name}")

    if not name or not name.strip():
        logger.error("Cannot update list with empty name")
        raise ValueError("List name cannot be empty")

    list_instance = get_list_by_id(list_id, session)
    if not list_instance:
        logger.error(f"Cannot update list: list with id {list_id} not found")
        raise ValueError(f"List with id {list_id} not found")

    try:
        list_instance.name = name.strip()
        session.add(list_instance)
        session.commit()
        session.refresh(list_instance)

        logger.info(f"Successfully updated list with id: {list_id}, new name: {name}")
        return list_instance
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to update list '{name}': unique constraint violation - {e}")
        raise ValueError(f"List with name '{name}' already exists") from e


def delete_list(list_id: int, session: Session) -> bool:
    """
    Delete a list by its ID.

    Args:
        list_id: ID of the list to delete
        session: Database session

    Returns:
        bool: True if list was deleted, False if list was not found

    Raises:
        IntegrityError: If list has associated tasks (foreign key constraint violation)
    """
    logger.info(f"Deleting list with id: {list_id}")

    list_instance = get_list_by_id(list_id, session)
    if not list_instance:
        logger.warning(f"Cannot delete list: list with id {list_id} not found")
        return False

    try:
        session.delete(list_instance)
        session.commit()

        logger.info(f"Successfully deleted list with id: {list_id}")
        return True
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to delete list with id {list_id}: foreign key constraint violation - {e}")
        raise ValueError(f"Cannot delete list with id {list_id}: it has associated tasks") from e


def get_system_lists(session: Session) -> list[List]:
    """
    Get all system lists from the database.

    Args:
        session: Database session

    Returns:
        list[List]: List of all system List instances
    """
    logger.info("Fetching all system lists")

    statement = select(List).where(List.is_system == True)  # noqa: E712
    lists = session.exec(statement).all()

    logger.info(f"Found {len(lists)} system lists")
    return list(lists)


def get_or_create_system_list(name: str, session: Session) -> List:
    """
    Get an existing system list by name, or create it if it doesn't exist.

    Args:
        name: Name of the system list
        session: Database session

    Returns:
        List: The existing or newly created system list instance
    """
    logger.info(f"Getting or creating system list with name: {name}")

    # Try to find existing system list with this name
    statement = select(List).where(List.name == name, List.is_system == True)  # noqa: E712
    list_instance = session.exec(statement).first()

    if list_instance:
        logger.info(f"Found existing system list with name: {name}, id: {list_instance.id}")
        return list_instance

    # Create new system list
    logger.info(f"Creating new system list with name: {name}")
    try:
        new_list = List(name=name.strip(), is_system=True)
        session.add(new_list)
        session.commit()
        session.refresh(new_list)

        logger.info(f"Successfully created system list with id: {new_list.id}, name: {name}")
        return new_list
    except IntegrityError as e:
        session.rollback()
        # If we get a unique constraint violation, try to fetch it again
        # (race condition scenario)
        logger.warning(f"Race condition detected while creating system list '{name}', retrying fetch")
        statement = select(List).where(List.name == name, List.is_system == True)  # noqa: E712
        list_instance = session.exec(statement).first()
        if list_instance:
            logger.info(f"Found system list after race condition: {name}, id: {list_instance.id}")
            return list_instance
        logger.error(f"Failed to create system list '{name}': {e}")
        raise ValueError(f"Failed to create system list '{name}'") from e
