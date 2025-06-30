import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler

class LevelnameColorFormatter(logging.Formatter):
    """Formatter that only colorizes the levelname"""
    
    # ANSI color codes
    COLOR_CODES = {
        logging.DEBUG: "\033[36m",    # Cyan
        logging.INFO: "\033[32m",     # Green
        logging.WARNING: "\033[33m",  # Yellow
        logging.ERROR: "\033[31m",    # Red
        logging.CRITICAL: "\033[31;1m"  # Bright red
    }
    RESET_CODE = "\033[0m"
    
    def format(self, record):
        # Get the original formatted message
        message = super().format(record)
        
        # Colorize only the levelname
        if record.levelno in self.COLOR_CODES:
            colored_levelname = (
                f"{self.COLOR_CODES[record.levelno]}{record.levelname}{self.RESET_CODE}"
            )
            message = message.replace(record.levelname, colored_levelname)
        
        return message

class AppLogger:
    def __init__(self, name: str = "app"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Console handler with levelname colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Standard format with colorized levelname
        console_formatter = LevelnameColorFormatter(
            "%(levelname)s : %(asctime)s - %(name)s  - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler (no colors)
        file_handler = RotatingFileHandler(
            logs_dir / "app.log",
            maxBytes=1024 * 1024,
            backupCount=10,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(levelname)s : %(asctime)s - %(name)s  - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        return self.logger

# Initialize logger
logger = AppLogger().get_logger()