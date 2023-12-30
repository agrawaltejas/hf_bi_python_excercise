import logging
from logging.handlers import RotatingFileHandler


def get_logger(file_name):
    """
    Creates and returns a logger instance.

    Args:
        file_name (str): The name of the file for which the logger is being created.
                         This is used to name the logger.

    Returns:
        logging.Logger: A configured logger instance for the given file name.
    """

    # Create a logger with the given name
    logger = logging.getLogger(file_name)

    # Set the log level
    logger.setLevel(logging.INFO)

    # Create formatter for logging messages
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Create a file handler which logs even debug messages
    file_handler = RotatingFileHandler(
        "recipe_processing.log", maxBytes=1048576, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create a console handler to output logs to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
