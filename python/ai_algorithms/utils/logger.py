"""
Logging utilities
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(
    name: str = "dental_ai",
    log_dir: str = "logs",
    log_level: int = logging.INFO
) -> logging.Logger:
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        log_dir: Directory to save log files
        log_level: Logging level
        
    Returns:
        Configured logger
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create log directory
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    simple_formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    # File handler
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_handler = logging.FileHandler(
        log_path / f"{name}_{timestamp}.log"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(detailed_formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger


class TensorBoardLogger:
    """
    TensorBoard logging wrapper
    """
    
    def __init__(self, log_dir: str = "runs"):
        from torch.utils.tensorboard import SummaryWriter
        self.writer = SummaryWriter(log_dir)
        
    def log_scalar(self, tag: str, value: float, step: int):
        """Log scalar value"""
        self.writer.add_scalar(tag, value, step)
    
    def log_scalars(self, tag: str, values: dict, step: int):
        """Log multiple scalar values"""
        self.writer.add_scalars(tag, values, step)
    
    def log_image(self, tag: str, image, step: int):
        """Log image"""
        self.writer.add_image(tag, image, step)
    
    def log_histogram(self, tag: str, values, step: int):
        """Log histogram"""
        self.writer.add_histogram(tag, values, step)
    
    def close(self):
        """Close writer"""
        self.writer.close()
