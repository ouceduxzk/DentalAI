"""
地标点检测模型
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class LandmarkDetectionModel(nn.Module):
    """
    地标点检测模型
    输入: 牙齿点云或图像
    输出: 关键点坐标
    """
    
    def __init__(self, num_landmarks=10, backbone='resnet', input_dim=3):
        super(LandmarkDetectionModel, self).__init__()
        
        self.num_landmarks = num_landmarks
        self.backbone = backbone
        
        # 特征提取器
        self.feature_extractor = self._build_backbone(input_dim)
        
        # 关键点回归头
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, num_landmarks * 3)  # (x, y, z) for each landmark
        
        self.dropout = nn.Dropout(0.5)
    
    def _build_backbone(self, input_dim):
        """构建特征提取主干网络"""
        return nn.Sequential(
            nn.Conv1d(input_dim, 64, 1),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            
            nn.Conv1d(64, 128, 1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            
            nn.Conv1d(128, 256, 1),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            
            nn.Conv1d(256, 512, 1),
            nn.BatchNorm1d(512),
            nn.ReLU()
        )
    
    def forward(self, x):
        """
        Args:
            x: (B, N, 3) 点云坐标
        
        Returns:
            landmarks: (B, num_landmarks, 3) 地标点坐标
        """
        B = x.shape[0]
        
        # 转置: (B, N, 3) -> (B, 3, N)
        x = x.transpose(1, 2)
        
        # 特征提取
        features = self.feature_extractor(x)  # (B, 512, N)
        
        # 全局池化
        features = torch.max(features, dim=2)[0]  # (B, 512)
        
        # 回归关键点
        x = F.relu(self.fc1(features))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        landmarks = self.fc3(x)  # (B, num_landmarks * 3)
        
        # 重塑为 (B, num_landmarks, 3)
        landmarks = landmarks.view(B, self.num_landmarks, 3)
        
        return landmarks


class HeatmapBasedLandmarkModel(nn.Module):
    """
    基于热图的地标点检测（用于2D图像）
    """
    
    def __init__(self, num_landmarks=10, input_channels=3):
        super(HeatmapBasedLandmarkModel, self).__init__()
        
        self.num_landmarks = num_landmarks
        
        # 编码器
        self.enc1 = self._conv_block(input_channels, 64)
        self.enc2 = self._conv_block(64, 128)
        self.enc3 = self._conv_block(128, 256)
        self.enc4 = self._conv_block(256, 512)
        
        self.pool = nn.MaxPool2d(2)
        
        # 解码器
        self.upconv3 = nn.ConvTranspose2d(512, 256, 2, stride=2)
        self.dec3 = self._conv_block(512, 256)
        
        self.upconv2 = nn.ConvTranspose2d(256, 128, 2, stride=2)
        self.dec2 = self._conv_block(256, 128)
        
        self.upconv1 = nn.ConvTranspose2d(128, 64, 2, stride=2)
        self.dec1 = self._conv_block(128, 64)
        
        # 输出热图
        self.out = nn.Conv2d(64, num_landmarks, 1)
    
    def _conv_block(self, in_channels, out_channels):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels, out_channels, 3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        """
        Args:
            x: (B, 3, H, W) 输入图像
        
        Returns:
            heatmaps: (B, num_landmarks, H, W) 每个地标点的热图
        """
        # 编码器
        enc1 = self.enc1(x)
        enc2 = self.enc2(self.pool(enc1))
        enc3 = self.enc3(self.pool(enc2))
        enc4 = self.enc4(self.pool(enc3))
        
        # 解码器
        dec3 = self.upconv3(enc4)
        dec3 = torch.cat([dec3, enc3], dim=1)
        dec3 = self.dec3(dec3)
        
        dec2 = self.upconv2(dec3)
        dec2 = torch.cat([dec2, enc2], dim=1)
        dec2 = self.dec2(dec2)
        
        dec1 = self.upconv1(dec2)
        dec1 = torch.cat([dec1, enc1], dim=1)
        dec1 = self.dec1(dec1)
        
        # 输出热图
        heatmaps = torch.sigmoid(self.out(dec1))
        
        return heatmaps
