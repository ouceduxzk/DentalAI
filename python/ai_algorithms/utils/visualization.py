"""
Visualization utilities for results
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Optional, List
import torch


def visualize_results(
    images: np.ndarray,
    predictions: np.ndarray,
    targets: Optional[np.ndarray] = None,
    class_names: Optional[List[str]] = None,
    save_path: Optional[str] = None
):
    """
    Visualize model predictions
    
    Args:
        images: Input images [B, C, H, W]
        predictions: Predicted labels [B]
        targets: Ground truth labels [B] (optional)
        class_names: List of class names
        save_path: Path to save figure
    """
    batch_size = min(len(images), 16)
    rows = 4
    cols = 4
    
    fig, axes = plt.subplots(rows, cols, figsize=(15, 15))
    axes = axes.flatten()
    
    for idx in range(batch_size):
        ax = axes[idx]
        
        # Convert image to displayable format
        img = images[idx]
        if isinstance(img, torch.Tensor):
            img = img.cpu().numpy()
        
        # CHW to HWC
        if img.shape[0] == 3:
            img = img.transpose(1, 2, 0)
        
        # Denormalize if needed
        img = (img - img.min()) / (img.max() - img.min() + 1e-8)
        
        ax.imshow(img)
        
        # Add title with prediction and target
        pred_label = predictions[idx]
        title = f"Pred: {class_names[pred_label] if class_names else pred_label}"
        
        if targets is not None:
            target_label = targets[idx]
            title += f"\nGT: {class_names[target_label] if class_names else target_label}"
            
            # Color based on correctness
            color = 'green' if pred_label == target_label else 'red'
            ax.set_title(title, color=color)
        else:
            ax.set_title(title)
        
        ax.axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved visualization to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: Optional[List[str]] = None,
    save_path: Optional[str] = None
):
    """
    Plot confusion matrix
    
    Args:
        cm: Confusion matrix
        class_names: List of class names
        save_path: Path to save figure
    """
    plt.figure(figsize=(12, 10))
    
    # Normalize confusion matrix
    cm_normalized = cm.astype('float') / (cm.sum(axis=1)[:, np.newaxis] + 1e-10)
    
    sns.heatmap(
        cm_normalized,
        annot=True,
        fmt='.2f',
        cmap='Blues',
        xticklabels=class_names if class_names else range(len(cm)),
        yticklabels=class_names if class_names else range(len(cm)),
        cbar_kws={'label': 'Accuracy'}
    )
    
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved confusion matrix to {save_path}")
    else:
        plt.show()
    
    plt.close()


def plot_training_curves(
    train_losses: List[float],
    val_losses: Optional[List[float]] = None,
    train_accs: Optional[List[float]] = None,
    val_accs: Optional[List[float]] = None,
    save_path: Optional[str] = None
):
    """
    Plot training curves
    
    Args:
        train_losses: Training losses
        val_losses: Validation losses
        train_accs: Training accuracies
        val_accs: Validation accuracies
        save_path: Path to save figure
    """
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # Loss curves
    axes[0].plot(train_losses, label='Train Loss', linewidth=2)
    if val_losses:
        axes[0].plot(val_losses, label='Val Loss', linewidth=2)
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Accuracy curves
    if train_accs:
        axes[1].plot(train_accs, label='Train Acc', linewidth=2)
    if val_accs:
        axes[1].plot(val_accs, label='Val Acc', linewidth=2)
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy (%)')
    axes[1].set_title('Training and Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved training curves to {save_path}")
    else:
        plt.show()
    
    plt.close()


def visualize_segmentation(
    image: np.ndarray,
    pred_mask: np.ndarray,
    gt_mask: Optional[np.ndarray] = None,
    save_path: Optional[str] = None
):
    """
    Visualize segmentation results
    
    Args:
        image: Input image
        pred_mask: Predicted segmentation mask
        gt_mask: Ground truth mask (optional)
        save_path: Path to save figure
    """
    num_plots = 3 if gt_mask is not None else 2
    fig, axes = plt.subplots(1, num_plots, figsize=(5 * num_plots, 5))
    
    # Original image
    axes[0].imshow(image)
    axes[0].set_title('Input Image')
    axes[0].axis('off')
    
    # Predicted mask
    axes[1].imshow(pred_mask, cmap='tab20')
    axes[1].set_title('Predicted Segmentation')
    axes[1].axis('off')
    
    # Ground truth mask
    if gt_mask is not None:
        axes[2].imshow(gt_mask, cmap='tab20')
        axes[2].set_title('Ground Truth')
        axes[2].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Saved segmentation visualization to {save_path}")
    else:
        plt.show()
    
    plt.close()
