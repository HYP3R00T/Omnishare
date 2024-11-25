import logging
import os
from datetime import datetime
from functools import wraps

from rich.console import Console
from rich.logging import RichHandler

from omnishare.constants import LOG_DIR


def setup_logger(name="omnishare"):
    """Set up and return a logger with both console and file handlers."""
    # Create logs directory
    os.makedirs(LOG_DIR, exist_ok=True)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Clear any existing handlers
    logger.handlers = []

    # Console handler with Rich
    console_handler = RichHandler(
        console=Console(force_terminal=True),
        show_time=True,
        markup=True,
    )
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    # File handler
    log_file = os.path.join(LOG_DIR, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    return logger


def log_api_call(func):
    """Decorator to log API calls"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = setup_logger()

        try:
            logger.info(f"[blue]Calling {func.__name__}[/blue]")
            result = func(*args, **kwargs)

            if hasattr(result, "status_code"):
                status = result.status_code
                color = "green" if 200 <= status < 300 else "red"
                logger.info(f"[{color}]Response status: {status}[/{color}]")

            return result

        except Exception as e:
            logger.error(f"[red]Error in {func.__name__}: {str(e)}[/red]")
            raise

    return wrapper
