import logging
import os
from typing import Optional

# Constants for logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a configured logger instance.
    
    Args:
        name (Optional[str]): The name for the logger. If None, returns the root logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name or "blog_post_agent")
    
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
        logger.addHandler(console_handler)
        
        # Set log level
        try:
            logger.setLevel(LOG_LEVEL)
        except ValueError:
            logger.setLevel(logging.INFO)
            logger.warning(f"Invalid LOG_LEVEL: {LOG_LEVEL}, defaulting to INFO")
    
    return logger

# Create a default logger instance
logger = get_logger() 