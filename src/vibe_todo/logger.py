"""Logger configuration module using loguru."""

import os
import sys
from pathlib import Path
from typing import Literal

from loguru import logger


def configure_logger(
    environment: Literal["dev", "prod"] = "dev",
    log_level: str = "INFO",
    log_to_file: bool = False,
    log_file_path: str | Path | None = None,
) -> None:
    """
    Configure loguru logger for the application.

    Args:
        environment: Environment type ('dev' or 'prod')
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_to_file: Whether to log to a file
        log_file_path: Path to log file (defaults to logs/app.log)
    """
    # remove default handler
    logger.remove()

    # determine log format based on environment
    if environment == "dev":
        # development: more detailed format with colors
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    else:
        # production: simpler format without colors
        log_format = (
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{function}:{line} | "
            "{message}"
        )

    # add console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level=log_level,
        colorize=(environment == "dev"),
        backtrace=True,
        diagnose=(environment == "dev"),
    )

    # add file handler if requested
    if log_to_file:
        if log_file_path is None:
            # default log file location
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_file_path = log_dir / "app.log"
        else:
            log_file_path = Path(log_file_path)
            log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # file handler with rotation
        logger.add(
            log_file_path,
            format=log_format,
            level=log_level,
            rotation="10 MB",
            retention="7 days",
            compression="zip",
            backtrace=True,
            diagnose=(environment == "dev"),
        )


def setup_logger() -> None:
    """
    Setup logger based on environment variables or defaults.

    Reads LOG_ENV environment variable (defaults to 'dev').
    Reads LOG_LEVEL environment variable (defaults to 'INFO').
    Reads LOG_TO_FILE environment variable (defaults to False).
    """
    environment = os.getenv("LOG_ENV", "dev")
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_to_file = os.getenv("LOG_TO_FILE", "false").lower() == "true"

    # validate environment
    if environment not in ("dev", "prod"):
        environment = "dev"

    configure_logger(
        environment=environment,  # type: ignore[arg-type]
        log_level=log_level,
        log_to_file=log_to_file,
    )


# setup logger on module import
setup_logger()

# export logger instance for easy import
__all__ = ["logger", "configure_logger", "setup_logger"]
