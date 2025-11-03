# 牙齿分割 (Tooth Segmentation)

## 任务描述

从口腔 3D 扫描数据中自动分割出单个牙齿，为每个牙齿分配唯一的标签。

## 输入输出

- **输入**: 口腔 3D 扫描数据（点云或网格）
- **输出**: 每个点/面的牙齿标签（0=背景，1-32=牙齿编号）

## 模型架构

### 1. PointNet++ (点云分割)
- 适用于点云数据
- 层次化特征提取
- 参数量: ~1.5M

### 2. MeshSegNet (网格分割)
- 适用于三角网格数据
- 基于图卷积网络
- 参数量: ~2.1M

### 3. U-Net 3D (体素分割)
- 适用于体素化数据
- 编码器-解码器结构
- 参数量: ~7.8M

## 使用方法

### 训练

```bash
# 使用默认配置
python train.py

# 使用自定义配置
python train.py --config config.yaml

# 多GPU训练
python train.py --config config.yaml --gpus 0,1,2,3

# 从检查点继续训练
python train.py --resume checkpoints/latest.pth
```

### 推理

```bash
# 单个文件
python inference.py --model checkpoints/best.pth --input sample.obj --output result.obj

# 批量处理
python inference.py --model checkpoints/best.pth --input_dir data/test/ --output_dir results/

# 可视化结果
python inference.py --model checkpoints/best.pth --input sample.obj --visualize
```

## 配置说明

编辑 `config.yaml` 自定义训练参数：

```yaml
# 数据配置
data:
  train_path: "data/segmentation/train"
  val_path: "data/segmentation/val"
  num_points: 10000  # 采样点数
  num_classes: 33    # 32个牙齿 + 背景

# 模型配置
model:
  name: "pointnet++"
  backbone: "pointnet2_ssg"
  
# 训练配置
training:
  batch_size: 16
  epochs: 200
  learning_rate: 0.001
  optimizer: "adam"
```

## 数据准备

### 数据格式

```
data/segmentation/
├── train/
│   ├── scans/          # 原始扫描文件
│   │   ├── case001.obj
│   │   └── case002.obj
│   └── labels/         # 分割标签
│       ├── case001.json
│       └── case002.json
├── val/
└── test/
```

### 标签格式 (JSON)

```json
{
  "filename": "case001.obj",
  "num_points": 50000,
  "labels": [1, 1, 1, ..., 16, 16, 16],  # 每个点的标签
  "tooth_ids": [11, 12, 13, 14, 15, 16, ...]  # FDI编号
}
```

## 性能指标

| 指标 | 验证集 | 测试集 |
|------|--------|--------|
| mIoU | 91.5% | 90.8% |
| Dice | 94.2% | 93.7% |
| Accuracy | 96.3% | 95.9% |

## 预训练模型

下载预训练模型：

```bash
# PointNet++
wget https://example.com/models/segmentation_pointnet_best.pth

# MeshSegNet
wget https://example.com/models/segmentation_mesh_best.pth
```

## 常见问题

### Q: 如何处理牙齿缺失的情况？
A: 模型会自动跳过缺失的牙齿，只输出存在的牙齿标签。

### Q: 如何提高小牙齿的分割精度？
A: 增加采样点数，使用类别权重平衡，或使用 Focal Loss。

### Q: 支持哪些 3D 文件格式？
A: 目前支持 .obj, .ply, .stl 格式。

## 参考文献

1. Qi et al., "PointNet++: Deep Hierarchical Feature Learning on Point Sets"
2. Lian et al., "MeshSegNet: Deep Multi-Scale Mesh Feature Learning"
