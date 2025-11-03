"""
牙轴检测数据集
"""

import torch
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path
import json


class ToothAxisDataset(Dataset):
    """牙轴检测数据集"""
    
    def __init__(self, data_path, num_points=2048, augment=False):
        self.data_path = Path(data_path)
        self.num_points = num_points
        self.augment = augment
        self.samples = self._load_samples()
    
    def _load_samples(self):
        samples = []
        tooth_dir = self.data_path / 'teeth'
        axis_dir = self.data_path / 'axes'
        
        if not tooth_dir.exists():
            return samples
        
        for tooth_file in tooth_dir.glob('*.obj'):
            axis_file = axis_dir / f"{tooth_file.stem}.json"
            if axis_file.exists():
                samples.append({
                    'tooth': str(tooth_file),
                    'axis': str(axis_file)
                })
        
        return samples
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # 加载牙齿点云
        points = self._load_points(sample['tooth'])
        
        # 加载牙轴
        origin, direction = self._load_axis(sample['axis'])
        
        # 采样点
        if len(points) > self.num_points:
            indices = np.random.choice(len(points), self.num_points, replace=False)
            points = points[indices]
        elif len(points) < self.num_points:
            indices = np.random.choice(len(points), self.num_points, replace=True)
            points = points[indices]
        
        # 归一化
        centroid = points.mean(axis=0)
        points = points - centroid
        origin = origin - centroid
        
        max_dist = np.max(np.linalg.norm(points, axis=1))
        points = points / (max_dist + 1e-8)
        origin = origin / (max_dist + 1e-8)
        
        # 转为tensor
        points = torch.from_numpy(points).float()
        origin = torch.from_numpy(origin).float()
        direction = torch.from_numpy(direction).float()
        
        return points, origin, direction
    
    def _load_points(self, tooth_path):
        vertices = []
        with open(tooth_path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    vertices.append(vertex)
        return np.array(vertices, dtype=np.float32)
    
    def _load_axis(self, axis_path):
        with open(axis_path, 'r') as f:
            data = json.load(f)
        origin = np.array(data['origin'], dtype=np.float32)
        direction = np.array(data['direction'], dtype=np.float32)
        # 归一化方向向量
        direction = direction / (np.linalg.norm(direction) + 1e-8)
        return origin, direction
