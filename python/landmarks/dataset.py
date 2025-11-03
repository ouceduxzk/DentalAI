"""
地标点检测数据集
"""

import torch
from torch.utils.data import Dataset
import numpy as np
from pathlib import Path
import json


class LandmarkDataset(Dataset):
    """
    地标点检测数据集
    """
    
    def __init__(self, data_path, num_points=2048, augment=False):
        self.data_path = Path(data_path)
        self.num_points = num_points
        self.augment = augment
        
        self.samples = self._load_samples()
    
    def _load_samples(self):
        samples = []
        
        scan_dir = self.data_path / 'scans'
        landmark_dir = self.data_path / 'landmarks'
        
        if not scan_dir.exists():
            return samples
        
        for scan_file in scan_dir.glob('*.obj'):
            landmark_file = landmark_dir / f"{scan_file.stem}.json"
            if landmark_file.exists():
                samples.append({
                    'scan': str(scan_file),
                    'landmarks': str(landmark_file)
                })
        
        return samples
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        sample = self.samples[idx]
        
        # 加载点云
        points = self._load_points(sample['scan'])
        
        # 加载地标点
        landmarks = self._load_landmarks(sample['landmarks'])
        
        # 采样
        if len(points) > self.num_points:
            indices = np.random.choice(len(points), self.num_points, replace=False)
            points = points[indices]
        elif len(points) < self.num_points:
            indices = np.random.choice(len(points), self.num_points, replace=True)
            points = points[indices]
        
        # 归一化
        centroid = points.mean(axis=0)
        points = points - centroid
        landmarks = landmarks - centroid
        
        max_dist = np.max(np.linalg.norm(points, axis=1))
        points = points / (max_dist + 1e-8)
        landmarks = landmarks / (max_dist + 1e-8)
        
        # 数据增强
        if self.augment:
            points, landmarks = self._augment(points, landmarks)
        
        points = torch.from_numpy(points).float()
        landmarks = torch.from_numpy(landmarks).float()
        
        return points, landmarks
    
    def _load_points(self, scan_path):
        vertices = []
        with open(scan_path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.strip().split()
                    vertex = [float(parts[1]), float(parts[2]), float(parts[3])]
                    vertices.append(vertex)
        return np.array(vertices, dtype=np.float32)
    
    def _load_landmarks(self, landmark_path):
        with open(landmark_path, 'r') as f:
            data = json.load(f)
        landmarks = np.array(data['landmarks'], dtype=np.float32)
        return landmarks
    
    def _augment(self, points, landmarks):
        # 随机旋转
        if np.random.random() > 0.5:
            theta = np.random.uniform(0, 2 * np.pi)
            rotation_matrix = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ], dtype=np.float32)
            points = points @ rotation_matrix.T
            landmarks = landmarks @ rotation_matrix.T
        
        return points, landmarks
