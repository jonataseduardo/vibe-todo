"""Services module for business logic and database operations."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import func
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

    try:
        statement = select(List)
        lists = session.exec(statement).all()

        logger.info(f"Found {len(lists)} lists")
        return list(lists)
    except Exception as e:
        logger.error(f"Failed to fetch all lists: {e}")
        raise


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

    try:
        statement = select(List).where(List.id == list_id)
        list_instance = session.exec(statement).first()

        if list_instance:
            logger.info(f"Found list with id: {list_id}, name: {list_instance.name}")
        else:
            logger.warning(f"List with id: {list_id} not found")

        return list_instance
    except Exception as e:
        logger.error(f"Failed to fetch list with id {list_id}: {e}")
        raise


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

    try:
        statement = select(List).where(List.is_system == True)  # noqa: E712
        lists = session.exec(statement).all()

        logger.info(f"Found {len(lists)} system lists")
        return list(lists)
    except Exception as e:
        logger.error(f"Failed to fetch system lists: {e}")
        raise


def get_or_create_system_list(name: str, session: Session) -> List:
    """
    Get an existing system list by name, or create it if it doesn't exist.

    Args:
        name: Name of the system list
        session: Database session

    Returns:
        List: The existing or newly created system list instance

    Raises:
        ValueError: If name is empty or creation fails
    """
    logger.info(f"Getting or creating system list with name: {name}")

    if not name or not name.strip():
        logger.error("Cannot get or create system list with empty name")
        raise ValueError("System list name cannot be empty")

    try:
        # Try to find existing system list with this name
        statement = select(List).where(List.name == name, List.is_system == True)  # noqa: E712
        list_instance = session.exec(statement).first()

        if list_instance:
            logger.info(f"Found existing system list with name: {name}, id: {list_instance.id}")
            return list_instance

        # Create new system list
        logger.info(f"Creating new system list with name: {name}")
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
        try:
            statement = select(List).where(List.name == name, List.is_system == True)  # noqa: E712
            list_instance = session.exec(statement).first()
            if list_instance:
                logger.info(f"Found system list after race condition: {name}, id: {list_instance.id}")
                return list_instance
        except Exception as fetch_error:
            logger.error(f"Failed to fetch system list after race condition: {fetch_error}")
        logger.error(f"Failed to create system list '{name}': {e}")
        raise ValueError(f"Failed to create system list '{name}'") from e
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to get or create system list '{name}': {e}")
        raise


# ============================================================================
# Task Service Functions
# ============================================================================


def create_task(list_id: int, title: str, session: Session, **kwargs) -> Task:
    """
    Create a new task.

    Args:
        list_id: ID of the list to associate the task with
        title: Title of the task
        session: Database session
        **kwargs: Additional task fields (description, due_date, is_completed, is_important)

    Returns:
        Task: The created task instance

    Raises:
        ValueError: If list_id is invalid or title is empty
        IntegrityError: If list_id doesn't exist (foreign key constraint violation)
    """
    logger.info(f"Creating task with list_id: {list_id}, title: {title}")

    if not title or not title.strip():
        logger.error("Cannot create task with empty title")
        raise ValueError("Task title cannot be empty")

    # Verify list exists
    list_instance = get_list_by_id(list_id, session)
    if not list_instance:
        logger.error(f"Cannot create task: list with id {list_id} not found")
        raise ValueError(f"List with id {list_id} not found")

    try:
        new_task = Task(
            list_id=list_id,
            title=title.strip(),
            description=kwargs.get("description"),
            due_date=kwargs.get("due_date"),
            is_completed=kwargs.get("is_completed", False),
            is_important=kwargs.get("is_important", False),
        )
        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        logger.info(f"Successfully created task with id: {new_task.id}, title: {title}")
        return new_task
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to create task: {e}")
        raise ValueError(f"Failed to create task: {e}") from e


def get_task_by_id(task_id: int, session: Session) -> Task | None:
    """
    Get a task by its ID.

    Args:
        task_id: ID of the task to retrieve
        session: Database session

    Returns:
        Task | None: The Task instance if found, None otherwise
    """
    logger.info(f"Fetching task with id: {task_id}")

    try:
        statement = select(Task).where(Task.id == task_id)
        task_instance = session.exec(statement).first()

        if task_instance:
            logger.info(f"Found task with id: {task_id}, title: {task_instance.title}")
        else:
            logger.warning(f"Task with id: {task_id} not found")

        return task_instance
    except Exception as e:
        logger.error(f"Failed to fetch task with id {task_id}: {e}")
        raise


def get_tasks_by_list(list_id: int, session: Session) -> list[Task]:
    """
    Get all tasks for a specific list.

    Args:
        list_id: ID of the list to retrieve tasks for
        session: Database session

    Returns:
        list[Task]: List of all Task instances for the specified list

    Raises:
        ValueError: If list_id is invalid or list not found
    """
    logger.info(f"Fetching tasks for list_id: {list_id}")

    # Validate list exists
    list_instance = get_list_by_id(list_id, session)
    if not list_instance:
        logger.error(f"Cannot fetch tasks: list with id {list_id} not found")
        raise ValueError(f"List with id {list_id} not found")

    try:
        statement = select(Task).where(Task.list_id == list_id)
        tasks = session.exec(statement).all()

        logger.info(f"Found {len(tasks)} tasks for list_id: {list_id}")
        return list(tasks)
    except Exception as e:
        logger.error(f"Failed to fetch tasks for list_id {list_id}: {e}")
        raise


def update_task(task_id: int, session: Session, **kwargs) -> Task:
    """
    Update an existing task.

    Args:
        task_id: ID of the task to update
        session: Database session
        **kwargs: Task fields to update (title, description, due_date, is_completed, is_important, list_id)

    Returns:
        Task: The updated task instance

    Raises:
        ValueError: If task not found or invalid update values
        IntegrityError: If list_id doesn't exist (foreign key constraint violation)
    """
    logger.info(f"Updating task with id: {task_id}")

    task_instance = get_task_by_id(task_id, session)
    if not task_instance:
        logger.error(f"Cannot update task: task with id {task_id} not found")
        raise ValueError(f"Task with id {task_id} not found")

    # Validate title if provided
    if "title" in kwargs:
        if not kwargs["title"] or not kwargs["title"].strip():
            logger.error("Cannot update task with empty title")
            raise ValueError("Task title cannot be empty")
        task_instance.title = kwargs["title"].strip()

    # Validate list_id if provided
    if "list_id" in kwargs:
        list_instance = get_list_by_id(kwargs["list_id"], session)
        if not list_instance:
            logger.error(f"Cannot update task: list with id {kwargs['list_id']} not found")
            raise ValueError(f"List with id {kwargs['list_id']} not found")
        task_instance.list_id = kwargs["list_id"]

    # Update other fields if provided
    if "description" in kwargs:
        task_instance.description = kwargs["description"]
    if "due_date" in kwargs:
        task_instance.due_date = kwargs["due_date"]
    if "is_completed" in kwargs:
        task_instance.is_completed = kwargs["is_completed"]
    if "is_important" in kwargs:
        task_instance.is_important = kwargs["is_important"]

    # Update timestamp
    task_instance.updated_at = datetime.now()

    try:
        session.add(task_instance)
        session.commit()
        session.refresh(task_instance)

        logger.info(f"Successfully updated task with id: {task_id}")
        return task_instance
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to update task with id {task_id}: integrity constraint violation - {e}")
        raise ValueError(f"Failed to update task: {e}") from e
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to update task with id {task_id}: {e}")
        raise


def delete_task(task_id: int, session: Session) -> bool:
    """
    Delete a task by its ID.

    Args:
        task_id: ID of the task to delete
        session: Database session

    Returns:
        bool: True if task was deleted, False if task was not found
    """
    logger.info(f"Deleting task with id: {task_id}")

    task_instance = get_task_by_id(task_id, session)
    if not task_instance:
        logger.warning(f"Cannot delete task: task with id {task_id} not found")
        return False

    try:
        session.delete(task_instance)
        session.commit()

        logger.info(f"Successfully deleted task with id: {task_id}")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to delete task with id {task_id}: {e}")
        raise


def toggle_complete(task_id: int, session: Session) -> Task:
    """
    Toggle the completion status of a task.

    Args:
        task_id: ID of the task to toggle
        session: Database session

    Returns:
        Task: The updated task instance

    Raises:
        ValueError: If task not found
    """
    logger.info(f"Toggling completion status for task with id: {task_id}")

    task_instance = get_task_by_id(task_id, session)
    if not task_instance:
        logger.error(f"Cannot toggle task: task with id {task_id} not found")
        raise ValueError(f"Task with id {task_id} not found")

    old_status = task_instance.is_completed
    task_instance.is_completed = not task_instance.is_completed

    # Update timestamp
    task_instance.updated_at = datetime.now()

    try:
        session.add(task_instance)
        session.commit()
        session.refresh(task_instance)

        logger.info(f"Successfully toggled completion status for task with id: {task_id}, is_completed: {old_status} -> {task_instance.is_completed}")
        return task_instance
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to toggle completion status for task with id {task_id}: {e}")
        raise


def toggle_important(task_id: int, session: Session) -> Task:
    """
    Toggle the important status of a task.

    Args:
        task_id: ID of the task to toggle
        session: Database session

    Returns:
        Task: The updated task instance

    Raises:
        ValueError: If task not found
    """
    logger.info(f"Toggling important status for task with id: {task_id}")

    task_instance = get_task_by_id(task_id, session)
    if not task_instance:
        logger.error(f"Cannot toggle task: task with id {task_id} not found")
        raise ValueError(f"Task with id {task_id} not found")

    old_status = task_instance.is_important
    task_instance.is_important = not task_instance.is_important

    # Update timestamp
    task_instance.updated_at = datetime.now()

    try:
        session.add(task_instance)
        session.commit()
        session.refresh(task_instance)

        logger.info(f"Successfully toggled important status for task with id: {task_id}, is_important: {old_status} -> {task_instance.is_important}")
        return task_instance
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to toggle important status for task with id {task_id}: {e}")
        raise


def get_important_tasks(session: Session) -> list[Task]:
    """
    Get all tasks marked as important.

    Args:
        session: Database session

    Returns:
        list[Task]: List of all Task instances marked as important
    """
    logger.info("Fetching all important tasks")

    try:
        statement = select(Task).where(Task.is_important == True)  # noqa: E712
        tasks = session.exec(statement).all()

        logger.info(f"Found {len(tasks)} important tasks")
        return list(tasks)
    except Exception as e:
        logger.error(f"Failed to fetch important tasks: {e}")
        raise


def get_planned_tasks(session: Session) -> list[Task]:
    """
    Get all tasks with a due date set (planned tasks).

    Args:
        session: Database session

    Returns:
        list[Task]: List of all Task instances with due_date set
    """
    logger.info("Fetching all planned tasks")

    try:
        statement = select(Task).where(Task.due_date.isnot(None))
        tasks = session.exec(statement).all()

        logger.info(f"Found {len(tasks)} planned tasks")
        return list(tasks)
    except Exception as e:
        logger.error(f"Failed to fetch planned tasks: {e}")
        raise


def get_all_tasks(session: Session, filters: dict | None = None) -> list[Task]:
    """
    Get all tasks with optional filters.

    Args:
        session: Database session
        filters: Optional dictionary of filter conditions. Supported keys:
            - list_id: Filter by list ID
            - is_completed: Filter by completion status (bool)
            - is_important: Filter by important status (bool)
            - due_date: Filter by due date (date)
            - title: Filter by title (substring match, case-insensitive)

    Returns:
        list[Task]: List of all Task instances matching the filters

    Raises:
        ValueError: If list_id in filters is invalid or list not found
    """
    logger.info("Fetching all tasks" + (f" with filters: {filters}" if filters else ""))

    # Validate list_id if provided in filters
    if filters and "list_id" in filters:
        list_instance = get_list_by_id(filters["list_id"], session)
        if not list_instance:
            logger.error(f"Cannot fetch tasks: list with id {filters['list_id']} not found")
            raise ValueError(f"List with id {filters['list_id']} not found")

    try:
        statement = select(Task)

        if filters:
            if "list_id" in filters:
                statement = statement.where(Task.list_id == filters["list_id"])
            if "is_completed" in filters:
                statement = statement.where(Task.is_completed == filters["is_completed"])
            if "is_important" in filters:
                statement = statement.where(Task.is_important == filters["is_important"])
            if "due_date" in filters:
                statement = statement.where(Task.due_date == filters["due_date"])
            if "title" in filters:
                # Case-insensitive substring match
                title_filter = filters["title"].strip()
                if title_filter:
                    statement = statement.where(func.lower(Task.title).like(f"%{title_filter.lower()}%"))

        tasks = session.exec(statement).all()

        logger.info(f"Found {len(tasks)} tasks" + (f" matching filters" if filters else ""))
        return list(tasks)
    except ValueError:
        # Re-raise ValueError (from list_id validation)
        raise
    except Exception as e:
        logger.error(f"Failed to fetch tasks: {e}")
        raise


def get_my_day_tasks(task_date: date, session: Session) -> list[Task]:
    """
    Get all tasks added to My Day for a specific date.

    Args:
        task_date: Date to retrieve My Day tasks for
        session: Database session

    Returns:
        list[Task]: List of all Task instances for the specified date
    """
    logger.info(f"Fetching My Day tasks for date: {task_date}")

    try:
        statement = (
            select(Task)
            .join(MyDayTask, Task.id == MyDayTask.task_id)
            .where(MyDayTask.task_date == task_date)
        )
        tasks = session.exec(statement).all()

        logger.info(f"Found {len(tasks)} My Day tasks for date: {task_date}")
        return list(tasks)
    except Exception as e:
        logger.error(f"Failed to fetch My Day tasks for date {task_date}: {e}")
        raise


def add_to_my_day(task_id: int, task_date: date, session: Session) -> MyDayTask:
    """
    Add a task to My Day for a specific date.

    Args:
        task_id: ID of the task to add
        task_date: Date to add the task to
        session: Database session

    Returns:
        MyDayTask: The created MyDayTask instance

    Raises:
        ValueError: If task not found or already added to My Day for this date
        IntegrityError: If task_id doesn't exist (foreign key constraint violation)
    """
    logger.info(f"Adding task {task_id} to My Day for date: {task_date}")

    # Verify task exists
    task_instance = get_task_by_id(task_id, session)
    if not task_instance:
        logger.error(f"Cannot add to My Day: task with id {task_id} not found")
        raise ValueError(f"Task with id {task_id} not found")

    # Check if already added
    statement = select(MyDayTask).where(
        MyDayTask.task_id == task_id,
        MyDayTask.task_date == task_date
    )
    existing = session.exec(statement).first()
    if existing:
        logger.warning(f"Task {task_id} already in My Day for date {task_date}")
        return existing

    try:
        my_day_task = MyDayTask(task_id=task_id, task_date=task_date)
        session.add(my_day_task)
        session.commit()
        session.refresh(my_day_task)

        logger.info(f"Successfully added task {task_id} to My Day for date: {task_date}")
        return my_day_task
    except IntegrityError as e:
        session.rollback()
        logger.error(f"Failed to add task to My Day: {e}")
        raise ValueError(f"Failed to add task to My Day: {e}") from e


def remove_from_my_day(task_id: int, task_date: date, session: Session) -> bool:
    """
    Remove a task from My Day for a specific date.

    Args:
        task_id: ID of the task to remove
        task_date: Date to remove the task from
        session: Database session

    Returns:
        bool: True if task was removed, False if task was not found in My Day for this date

    Raises:
        ValueError: If task_id is invalid or task not found
    """
    logger.info(f"Removing task {task_id} from My Day for date: {task_date}")

    # Validate task exists
    task_instance = get_task_by_id(task_id, session)
    if not task_instance:
        logger.error(f"Cannot remove from My Day: task with id {task_id} not found")
        raise ValueError(f"Task with id {task_id} not found")

    try:
        statement = select(MyDayTask).where(
            MyDayTask.task_id == task_id,
            MyDayTask.task_date == task_date
        )
        my_day_task = session.exec(statement).first()

        if not my_day_task:
            logger.warning(f"Task {task_id} not found in My Day for date {task_date}")
            return False

        session.delete(my_day_task)
        session.commit()

        logger.info(f"Successfully removed task {task_id} from My Day for date: {task_date}")
        return True
    except ValueError:
        # Re-raise ValueError (from task_id validation)
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to remove task {task_id} from My Day for date {task_date}: {e}")
        raise
