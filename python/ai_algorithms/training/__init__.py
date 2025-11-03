"""
Training module for AI models

This module contains training scripts, configurations, and utilities
for training deep learning models on dental data.
"""

from .trainer import Trainer
from .config import TrainingConfig

__all__ = ["Trainer", "TrainingConfig"]
