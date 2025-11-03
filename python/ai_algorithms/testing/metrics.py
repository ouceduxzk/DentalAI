"""
Evaluation metrics for dental AI models
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    roc_auc_score
)
from typing import Dict, Optional


def calculate_metrics(
    predictions: np.ndarray,
    targets: np.ndarray,
    probabilities: Optional[np.ndarray] = None,
    num_classes: Optional[int] = None
) -> Dict[str, float]:
    """
    Calculate comprehensive evaluation metrics
    
    Args:
        predictions: Predicted labels
        targets: Ground truth labels
        probabilities: Predicted probabilities (for AUC calculation)
        num_classes: Number of classes
        
    Returns:
        Dictionary containing various metrics
    """
    metrics = {}
    
    # Accuracy
    metrics['accuracy'] = accuracy_score(targets, predictions) * 100
    
    # Precision, Recall, F1
    precision, recall, f1, _ = precision_recall_fscore_support(
        targets, predictions, average='weighted', zero_division=0
    )
    metrics['precision'] = precision * 100
    metrics['recall'] = recall * 100
    metrics['f1_score'] = f1 * 100
    
    # Per-class metrics
    precision_per_class, recall_per_class, f1_per_class, _ = \
        precision_recall_fscore_support(
            targets, predictions, average=None, zero_division=0
        )
    
    metrics['precision_per_class'] = precision_per_class.tolist()
    metrics['recall_per_class'] = recall_per_class.tolist()
    metrics['f1_per_class'] = f1_per_class.tolist()
    
    # Confusion matrix
    cm = confusion_matrix(targets, predictions)
    metrics['confusion_matrix'] = cm.tolist()
    
    # AUC (if probabilities provided)
    if probabilities is not None and num_classes is not None:
        try:
            # One-vs-rest AUC
            auc = roc_auc_score(
                targets, probabilities, 
                multi_class='ovr',
                average='weighted'
            )
            metrics['auc'] = auc
        except Exception as e:
            print(f"Could not calculate AUC: {e}")
    
    return metrics


def calculate_segmentation_metrics(
    pred_mask: np.ndarray,
    gt_mask: np.ndarray
) -> Dict[str, float]:
    """
    Calculate segmentation-specific metrics (for tooth segmentation)
    
    Args:
        pred_mask: Predicted segmentation mask
        gt_mask: Ground truth segmentation mask
        
    Returns:
        Dictionary containing segmentation metrics
    """
    metrics = {}
    
    # Flatten arrays
    pred = pred_mask.flatten()
    gt = gt_mask.flatten()
    
    # IoU (Intersection over Union)
    intersection = np.logical_and(pred, gt).sum()
    union = np.logical_or(pred, gt).sum()
    iou = intersection / (union + 1e-10)
    metrics['iou'] = iou * 100
    
    # Dice coefficient
    dice = 2 * intersection / (pred.sum() + gt.sum() + 1e-10)
    metrics['dice'] = dice * 100
    
    # Pixel accuracy
    pixel_acc = (pred == gt).mean()
    metrics['pixel_accuracy'] = pixel_acc * 100
    
    return metrics
