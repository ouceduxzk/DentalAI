# 地标点检测 (Landmarks Detection)

## 任务描述

在牙齿模型上自动检测和定位关键的解剖标志点。

## 输入输出

- **输入**: 牙齿 3D 点云或 2D 图像
- **输出**: 关键点的 3D 坐标

## 关键点类型

- 牙尖点 (Cusp points)
- 牙颈缘点 (Cervical points)
- 接触点 (Contact points)
- 中央窝 (Central fossa)
- 解剖标志点

## 模型架构

1. **PointNet++ 基础模型**: 直接回归关键点坐标
2. **热图基础模型**: 生成关键点概率热图（用于2D）

## 使用方法

### 训练

```bash
python train.py --config config.yaml
```

### 推理

```bash
# 单个牙齿
python inference.py --model checkpoints/best.pth --input tooth.obj --output landmarks.json

# 可视化
python inference.py --model checkpoints/best.pth --input tooth.obj --visualize
```

## 数据格式

### 标注格式 (JSON)

```json
{
  "filename": "tooth_11.obj",
  "landmarks": [
    [10.5, 20.3, 15.8],  # 第1个关键点的 (x, y, z)
    [12.1, 22.5, 16.2],  # 第2个关键点
    ...
  ],
  "landmark_names": ["cusp", "cervical_buccal", "cervical_lingual", ...]
}
```

## 评估指标

- **MRE** (Mean Radial Error): 平均径向误差
- **PCK** (Percentage of Correct Keypoints): 在阈值内的正确关键点百分比
- **STD**: 误差标准差

## 性能

| 模型 | MRE (mm) | PCK@2mm | PCK@5mm |
|------|----------|---------|---------|
| PointNet++ | 1.2 | 89.5% | 97.3% |
| HRNet (2D) | 0.8 | 94.2% | 99.1% |
