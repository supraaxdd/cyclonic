import logging
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

def logger_setup(name=None, log_to_file=True, log_file_path="logs/log_out.log"):
    """
    Sets up a logger with console and optional file handlers.
    
    :param name: Logger name (defaults to module name)
    :param log_level: Logging level (DEBUG, INFO, WARNING, etc.)
    :param log_to_file: Whether to write logs to a file
    :param log_file_path: File path to save logs
    :return: Configured logger instance
    """
    logger = logging.getLogger(name or Path(__file__).stem)
    
    load_dotenv()
    log_level = os.environ.get("LOG_LEVEL")

    if log_level == "INFO":
        log_level = logging.INFO
    elif log_level == "DEBUG":
        log_level = logging.DEBUG
    elif log_level == "WARN":
        log_level = logging.WARN
    elif log_level == "ERROR":
        log_level = logging.ERROR
    else: log_level = logging.INFO

    logger.setLevel(log_level)

    # Prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)s | [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler
    if log_to_file:
        Path(log_file_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file_path, mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger