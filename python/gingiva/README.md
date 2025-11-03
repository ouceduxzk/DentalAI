# 牙龈处理 (Gingiva)

## 任务描述

虚拟牙龈的重建、分割和动画模拟。

## 子任务

1. **牙龈分割**: 从口腔扫描中分割出牙龈组织
2. **虚拟牙龈重建**: 生成缺失的牙龈几何
3. **牙龈动画**: 模拟正畸治疗过程中的牙龈变化

## 文件结构

```
gingiva/
├── segmentation/     # 牙龈分割
├── reconstruction/   # 虚拟重建
├── animation/        # 动画模拟
└── README.md
```

## 使用方法

```bash
# 牙龈分割
python gingiva/segmentation/train.py

# 虚拟牙龈重建
python gingiva/reconstruction/generate.py --input scan.obj --output gingiva.obj
```
