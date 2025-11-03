"""
牙齿分割模型定义
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class PointNetSetAbstraction(nn.Module):
    """PointNet++ Set Abstraction层"""
    
    def __init__(self, npoint, radius, nsample, in_channel, mlp):
        super(PointNetSetAbstraction, self).__init__()
        self.npoint = npoint
        self.radius = radius
        self.nsample = nsample
        self.mlp_convs = nn.ModuleList()
        self.mlp_bns = nn.ModuleList()
        
        last_channel = in_channel
        for out_channel in mlp:
            self.mlp_convs.append(nn.Conv2d(last_channel, out_channel, 1))
            self.mlp_bns.append(nn.BatchNorm2d(out_channel))
            last_channel = out_channel
    
    def forward(self, xyz, points):
        # xyz: (B, N, 3)
        # points: (B, C, N)
        
        # 简化版实现
        B, N, C = xyz.shape
        
        # 随机采样
        if self.npoint < N:
            idx = torch.randperm(N)[:self.npoint]
            new_xyz = xyz[:, idx, :]
        else:
            new_xyz = xyz
        
        # 特征聚合
        if points is not None:
            new_points = points
            for i, conv in enumerate(self.mlp_convs):
                bn = self.mlp_bns[i]
                new_points = F.relu(bn(conv(new_points.unsqueeze(-1))))
            new_points = torch.max(new_points, 2)[0]
        else:
            new_points = None
        
        return new_xyz, new_points


class SegmentationModel(nn.Module):
    """
    点云分割模型（PointNet++ 风格）
    """
    
    def __init__(self, num_classes=33, model_type='pointnet++'):
        super(SegmentationModel, self).__init__()
        
        self.num_classes = num_classes
        self.model_type = model_type
        
        # 特征提取
        self.sa1 = PointNetSetAbstraction(1024, 0.1, 32, 3, [32, 32, 64])
        self.sa2 = PointNetSetAbstraction(256, 0.2, 32, 64, [64, 64, 128])
        self.sa3 = PointNetSetAbstraction(64, 0.4, 32, 128, [128, 128, 256])
        
        # 全局特征
        self.fc1 = nn.Linear(256, 512)
        self.bn1 = nn.BatchNorm1d(512)
        self.drop1 = nn.Dropout(0.5)
        
        # 分割头
        self.fc2 = nn.Linear(512, 256)
        self.bn2 = nn.BatchNorm1d(256)
        self.drop2 = nn.Dropout(0.5)
        
        self.fc3 = nn.Linear(256, num_classes)
    
    def forward(self, xyz):
        """
        Args:
            xyz: (B, N, 3) 点云坐标
        
        Returns:
            out: (B, num_classes, N) 每个点的分类logits
        """
        B, N, _ = xyz.shape
        
        # 提取特征
        l1_xyz, l1_points = self.sa1(xyz, None)
        l2_xyz, l2_points = self.sa2(l1_xyz, l1_points)
        l3_xyz, l3_points = self.sa3(l2_xyz, l2_points)
        
        # 全局特征
        if l3_points is not None:
            x = l3_points.mean(dim=-1)  # (B, C)
        else:
            x = l3_xyz.mean(dim=1)  # (B, 3)
        
        # MLP
        x = self.drop1(F.relu(self.bn1(self.fc1(x))))
        x = self.drop2(F.relu(self.bn2(self.fc2(x))))
        x = self.fc3(x)  # (B, num_classes)
        
        # 扩展到每个点
        out = x.unsqueeze(2).expand(-1, -1, N)  # (B, num_classes, N)
        
        return out


class MeshSegNet(nn.Module):
    """
    基于图卷积的网格分割模型
    """
    
    def __init__(self, num_classes=33, num_channels=15):
        super(MeshSegNet, self).__init__()
        
        self.num_classes = num_classes
        
        # MeshConv layers (简化实现)
        self.conv1 = nn.Conv1d(num_channels, 64, 1)
        self.conv2 = nn.Conv1d(64, 128, 1)
        self.conv3 = nn.Conv1d(128, 256, 1)
        
        self.bn1 = nn.BatchNorm1d(64)
        self.bn2 = nn.BatchNorm1d(128)
        self.bn3 = nn.BatchNorm1d(256)
        
        # 分类头
        self.fc1 = nn.Conv1d(256, 128, 1)
        self.fc2 = nn.Conv1d(128, num_classes, 1)
        
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, x):
        """
        Args:
            x: (B, num_channels, N) 网格特征
        
        Returns:
            out: (B, num_classes, N)
        """
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.relu(self.bn3(self.conv3(x)))
        
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        out = self.fc2(x)
        
        return out
