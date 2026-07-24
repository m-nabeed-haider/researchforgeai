import sys

from loguru import logger


def configure_logger() -> None:
    """Configure Loguru for the application."""

    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        enqueue=True,
        backtrace=False,
        diagnose=False,
    )
