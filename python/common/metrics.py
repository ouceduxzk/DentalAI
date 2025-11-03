"""
评估指标
"""

import numpy as np
import torch


def segmentation_metrics(pred, target, num_classes):
    """
    计算分割指标
    
    Args:
        pred: (N,) 预测标签
        target: (N,) 真实标签
        num_classes: 类别数量
    
    Returns:
        dict: 包含各种指标的字典
    """
    metrics = {}
    
    # 整体准确率
    accuracy = (pred == target).sum() / len(pred)
    metrics['accuracy'] = accuracy
    
    # 每个类别的 IoU
    ious = []
    for c in range(num_classes):
        pred_mask = pred == c
        target_mask = target == c
        
        intersection = (pred_mask & target_mask).sum()
        union = (pred_mask | target_mask).sum()
        
        if union > 0:
            iou = intersection / union
            ious.append(iou)
    
    metrics['mean_iou'] = np.mean(ious) if ious else 0.0
    metrics['per_class_iou'] = ious
    
    # Dice系数
    dice_scores = []
    for c in range(num_classes):
        pred_mask = pred == c
        target_mask = target == c
        
        intersection = (pred_mask & target_mask).sum()
        dice = 2 * intersection / (pred_mask.sum() + target_mask.sum() + 1e-8)
        dice_scores.append(dice)
    
    metrics['mean_dice'] = np.mean(dice_scores) if dice_scores else 0.0
    
    return metrics


def landmark_metrics(pred_landmarks, gt_landmarks):
    """
    计算地标点检测指标
    
    Args:
        pred_landmarks: (N, 3) 预测的地标点
        gt_landmarks: (N, 3) 真实的地标点
    
    Returns:
        dict: 包含各种指标的字典
    """
    metrics = {}
    
    # Mean Radial Error (MRE)
    distances = np.linalg.norm(pred_landmarks - gt_landmarks, axis=1)
    mre = distances.mean()
    metrics['mre'] = mre
    metrics['std'] = distances.std()
    
    # Percentage of Correct Keypoints (PCK)
    thresholds = [1.0, 2.0, 3.0, 5.0]  # mm
    for threshold in thresholds:
        pck = (distances < threshold).mean()
        metrics[f'pck@{threshold}mm'] = pck
    
    return metrics


def axis_metrics(pred_origin, pred_direction, gt_origin, gt_direction):
    """
    计算牙轴检测指标
    
    Args:
        pred_origin: (3,) 预测的起点
        pred_direction: (3,) 预测的方向
        gt_origin: (3,) 真实的起点
        gt_direction: (3,) 真实的方向
    
    Returns:
        dict: 包含各种指标的字典
    """
    metrics = {}
    
    # Origin error
    origin_error = np.linalg.norm(pred_origin - gt_origin)
    metrics['origin_error'] = origin_error
    
    # Direction error (角度)
    pred_direction = pred_direction / (np.linalg.norm(pred_direction) + 1e-8)
    gt_direction = gt_direction / (np.linalg.norm(gt_direction) + 1e-8)
    
    cos_sim = np.dot(pred_direction, gt_direction)
    cos_sim = np.clip(cos_sim, -1.0, 1.0)
    angle_error = np.arccos(np.abs(cos_sim)) * 180 / np.pi
    
    metrics['angle_error_deg'] = angle_error
    
    return metrics


def compute_iou(pred_mask, gt_mask):
    """计算IoU"""
    intersection = (pred_mask & gt_mask).sum()
    union = (pred_mask | gt_mask).sum()
    return intersection / (union + 1e-8)


def compute_dice(pred_mask, gt_mask):
    """计算Dice系数"""
    intersection = (pred_mask & gt_mask).sum()
    return 2 * intersection / (pred_mask.sum() + gt_mask.sum() + 1e-8)
