"""
牙齿分割数据集
"""

import torch
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path
import json


class ToothSegmentationDataset(Dataset):
    """
    牙齿分割数据集
    """
    
    def __init__(self, data_path, num_points=10000, augment=False):
        self.data_path = Path(data_path)
        self.num_points = num_points
        self.augment = augment
        
        # 加载数据列表
        self.samples = self._load_samples()
    
    def _load_samples(self):
        """加载数据样本列表"""
        samples = []
        
        scan_dir = self.data_path / 'scans'
        label_dir = self.data_path / 'labels'
        
        if not scan_dir.exists():
            print(f"警告: {scan_dir} 不存在")
            return samples
        
        # 查找所有扫描文件
        for scan_file in scan_dir.glob('*.obj'):
            label_file = label_dir / f"{scan_file.stem}.json"
            if label_file.exists():
                samples.append({
                    'scan': str(scan_file),
                    'label': str(label_file)
                })
        
        return samples
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # 加载点云
        points = self._load_points(sample['scan'])
        
        # 加载标签
        labels = self._load_labels(sample['label'], len(points))
        
        # 采样固定数量的点
        if len(points) > self.num_points:
            indices = np.random.choice(len(points), self.num_points, replace=False)
            points = points[indices]
            labels = labels[indices]
        elif len(points) < self.num_points:
            # 重复采样
            indices = np.random.choice(len(points), self.num_points, replace=True)
            points = points[indices]
            labels = labels[indices]
        
        # 数据增强
        if self.augment:
            points = self._augment(points)
        
        # 转换为 tensor
        points = torch.from_numpy(points).float()
        labels = torch.from_numpy(labels).long()
        
        return points, labels
    
    def _load_points(self, scan_path):
        """加载点云数据"""
        # 简化实现：从 obj 文件读取顶点
        vertices = []
        
        with open(scan_path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    vertices.append(vertex)
        
        return np.array(vertices, dtype=np.float32)
    
    def _load_labels(self, label_path, num_points):
        """加载标签数据"""
        try:
            with open(label_path, 'r') as f:
                label_data = json.load(f)
            
            labels = np.array(label_data.get('labels', []), dtype=np.int64)
            
            # 如果标签数量不匹配，返回全0标签
            if len(labels) != num_points:
                print(f"警告: 标签数量 ({len(labels)}) 与点数量 ({num_points}) 不匹配")
                labels = np.zeros(num_points, dtype=np.int64)
        
        except Exception as e:
            print(f"加载标签失败: {e}")
            labels = np.zeros(num_points, dtype=np.int64)
        
        return labels
    
    def _augment(self, points):
        """数据增强"""
        # 随机旋转
        if np.random.random() > 0.5:
            theta = np.random.uniform(0, 2 * np.pi)
            rotation_matrix = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ], dtype=np.float32)
            points = points @ rotation_matrix.T
        
        # 随机缩放
        if np.random.random() > 0.5:
            scale = np.random.uniform(0.9, 1.1)
            points = points * scale
        
        # 随机抖动
        if np.random.random() > 0.5:
            jitter = np.random.normal(0, 0.01, points.shape).astype(np.float32)
            points = points + jitter
        
        # 归一化到单位球
        centroid = points.mean(axis=0)
        points = points - centroid
        max_dist = np.max(np.linalg.norm(points, axis=1))
        points = points / (max_dist + 1e-8)
        
        return points
