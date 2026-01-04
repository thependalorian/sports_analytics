"""
Logging Utility Module
Provides consistent logging across all modules
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path


class SportsAnalyticsLogger:
    """Centralized logging utility for sports analytics pipeline"""
    
    _logger = None
    _log_file = None
    
    @classmethod
    def setup_logger(cls, log_dir="logs", log_level=logging.INFO, log_to_file=True):
        """
        Setup logger with file and console handlers
        
        Args:
            log_dir: Directory for log files
            log_level: Logging level (default: INFO)
            log_to_file: Whether to log to file
        """
        if cls._logger is not None:
            return cls._logger
        
        # Create logger
        logger = logging.getLogger('sports_analytics')
        logger.setLevel(log_level)
        
        # Remove existing handlers
        logger.handlers = []
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        simple_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)
        
        # File handler
        if log_to_file:
            os.makedirs(log_dir, exist_ok=True)
            log_filename = f"analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            cls._log_file = os.path.join(log_dir, log_filename)
            
            file_handler = logging.FileHandler(cls._log_file)
            file_handler.setLevel(logging.DEBUG)  # More detailed in file
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
        
        cls._logger = logger
        return logger
    
    @classmethod
    def get_logger(cls):
        """
        Get the logger instance
        
        Returns:
            Logger instance
        """
        if cls._logger is None:
            cls.setup_logger()
        return cls._logger
    
    @classmethod
    def get_log_file(cls):
        """Get the current log file path"""
        return cls._log_file


def get_logger(name=None):
    """
    Get logger instance (convenience function)
    
    Args:
        name: Optional logger name
        
    Returns:
        Logger instance
    """
    if name:
        return logging.getLogger(f'sports_analytics.{name}')
    return SportsAnalyticsLogger.get_logger()

