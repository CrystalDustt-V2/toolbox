import logging
import sys
from pathlib import Path
from rich.logging import RichHandler

def setup_logging(level=logging.INFO, log_file: Path = None):
    """
    Setup structured logging using Rich for console and standard logging for files.
    """
    # Create logger
    logger = logging.getLogger("toolbox")
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers = []

    # Console handler (Rich)
    console_handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        show_time=False,
        show_path=False
    )
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # File handler (if provided)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Global logger instance
logger = logging.getLogger("toolbox")
