"""
牙轴检测模型
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class ToothAxisModel(nn.Module):
    """
    牙轴检测模型
    输入: 单个牙齿的点云
    输出: 牙轴向量 (origin + direction)
    """
    
    def __init__(self, backbone='pointnet', input_dim=3):
        super(ToothAxisModel, self).__init__()
        
        # 特征提取
        self.conv1 = nn.Conv1d(input_dim, 64, 1)
        self.conv2 = nn.Conv1d(64, 128, 1)
        self.conv3 = nn.Conv1d(128, 256, 1)
        self.conv4 = nn.Conv1d(256, 512, 1)
        
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(128)
        self.bn3 = nn.BatchNorm1d(256)
        self.bn4 = nn.BatchNorm1d(512)
        
        # 牙轴回归
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        
        # 输出：origin (3) + direction (3)
        self.fc_origin = nn.Linear(128, 3)
        self.fc_direction = nn.Linear(128, 3)
        
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        """
        Args:
            x: (B, N, 3) 牙齿点云
        
        Returns:
            origin: (B, 3) 牙轴起点
            direction: (B, 3) 牙轴方向（单位向量）
        """
        B = x.shape[0]
        
        # 转置
        x = x.transpose(1, 2)  # (B, 3, N)
        
        # 特征提取
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        x = F.relu(self.bn4(self.conv4(x)))
        
        # 全局特征
        x = torch.max(x, dim=2)[0]  # (B, 512)
        
        # MLP
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)
        
        # 预测 origin 和 direction
        origin = self.fc_origin(x)  # (B, 3)
        direction = self.fc_direction(x)  # (B, 3)
        
        # 归一化方向向量
        direction = F.normalize(direction, p=2, dim=1)
        
        return origin, direction


def angular_loss(pred_direction, gt_direction):
    """
    计算方向向量的角度损失
    
    Args:
        pred_direction: (B, 3) 预测的方向向量
        gt_direction: (B, 3) 真实的方向向量
    
    Returns:
        loss: 角度损失
    """
    # 归一化
    pred_direction = F.normalize(pred_direction, p=2, dim=1)
    gt_direction = F.normalize(gt_direction, p=2, dim=1)
    
    # 余弦相似度
    cos_sim = torch.sum(pred_direction * gt_direction, dim=1)
    
    # 角度损失 (1 - cos_similarity)
    loss = 1.0 - cos_sim.abs()  # 使用 abs 因为方向可能相反
    
    return loss.mean()
