import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    os.makedirs("logs", exist_ok=True)

    log_format = (
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    formatter = logging.Formatter(log_format)

    file_handler = RotatingFileHandler(
        filename="logs/error.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5
    )
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    root_logger.handlers.clear()

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
