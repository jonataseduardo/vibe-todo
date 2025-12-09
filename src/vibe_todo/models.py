"""SQLModel data models for the todo application."""

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    pass


class List(SQLModel, table=True):
    """List model representing a task list."""

    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    is_system: bool = Field(default=False)
    tasks: list["Task"] = Relationship(back_populates="task_list")


class Task(SQLModel, table=True):
    """Task model representing a todo task."""

    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    list_id: int = Field(foreign_key="list.id")
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    is_completed: bool = Field(default=False)
    is_important: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    task_list: Optional["List"] = Relationship(back_populates="tasks")
    subtasks: list["Subtask"] = Relationship(back_populates="task")
    my_day_entries: list["MyDayTask"] = Relationship(back_populates="task")


class Subtask(SQLModel, table=True):
    """Subtask model representing a subtask within a task."""

    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    title: str
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    task: Optional["Task"] = Relationship(back_populates="subtasks")


class MyDayTask(SQLModel, table=True):
    """MyDayTask model representing a many-to-many relationship between tasks and dates."""

    __table_args__ = {"extend_existing": True}

    task_id: int = Field(foreign_key="task.id", primary_key=True)
    task_date: date = Field(primary_key=True)
    task: Optional["Task"] = Relationship(back_populates="my_day_entries")
