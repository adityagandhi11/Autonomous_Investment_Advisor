"""Logging configuration."""

import logging


def setup_logger(name: str = "advisor", level=logging.INFO) -> logging.Logger:
    """Configure and return application logger."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console handler with formatting
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Global logger instance
logger = setup_logger()
