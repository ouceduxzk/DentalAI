# 牙轴检测 (Tooth Axis Detection)

## 任务描述

自动检测牙齿的长轴方向和位置，用于正畸治疗规划。

## 输入输出

- **输入**: 单个牙齿的 3D 点云
- **输出**: 
  - 牙轴起点坐标 (origin)
  - 牙轴方向向量 (direction, 单位向量)

## 牙轴定义

牙轴通常定义为：
- **起点**: 牙根尖点
- **方向**: 从根尖指向牙冠的方向
- 用于计算牙齿的倾斜角度、扭转角度等

## 模型架构

基于 PointNet 的回归网络：
- 输入: (N, 3) 点云
- 输出: origin (3,) + direction (3,)

## 损失函数

组合损失:
```python
loss = loss_origin + λ * loss_direction
```

- **loss_origin**: MSE loss for origin point
- **loss_direction**: Angular loss (1 - |cos(θ)|)

## 使用方法

### 训练

```bash
python train.py --config config.yaml
```

### 推理

```bash
# 单个牙齿
python inference.py --model checkpoints/best.pth --input tooth.obj

# 批量处理
python inference.py --model checkpoints/best.pth --input_dir data/teeth/ --output_dir results/
```

## 数据格式

### 标注格式 (JSON)

```json
{
  "filename": "tooth_11.obj",
  "origin": [10.5, 20.3, 15.8],
  "direction": [0.1, 0.2, 0.97],  # 单位向量
  "tooth_id": 11
}
```

## 评估指标

- **Origin Error**: 起点位置误差 (mm)
- **Angle Error**: 方向角度误差 (度)

## 性能

| 模型 | Origin Error (mm) | Angle Error (°) |
|------|-------------------|-----------------|
| PointNet | 0.8 | 3.2 |
| PointNet++ | 0.6 | 2.5 |

## 应用

- 正畸治疗规划
- 牙齿移动模拟
- 倾斜角度分析
- 扭转角度测量
