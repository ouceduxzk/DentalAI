"""
Testing and evaluation module

This module contains scripts for model evaluation, testing,
and inference on dental models.
"""

from .evaluator import Evaluator
from .metrics import calculate_metrics

__all__ = ["Evaluator", "calculate_metrics"]
