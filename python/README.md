# Python AI 算法模块

这个文件夹包含了牙科模型分析的所有 AI 算法，按照不同的任务进行组织。

## 目录结构

```
python/
├── segmentation/          # 牙齿分割
│   ├── train.py          # 训练脚本
│   ├── inference.py      # 推理脚本
│   ├── model.py          # 模型定义
│   ├── dataset.py        # 数据集加载
│   ├── config.yaml       # 配置文件
│   └── README.md         # 任务说明
├── landmarks/            # 地标点检测
├── tooth_axis/           # 牙轴检测
├── root_simulation/      # 牙根模拟
├── gingiva/             # 牙龈重建和动画
├── classification/       # 牙齿分类（角度分类等）
├── reconstruction/       # 3D 重建
├── common/              # 通用工具和模块
│   ├── utils.py         # 工具函数
│   ├── metrics.py       # 评估指标
│   ├── visualization.py # 可视化工具
│   └── base_trainer.py  # 基础训练器
├── requirements.txt     # Python 依赖
├── setup.py            # 安装配置
└── README.md           # 本文档
```

## AI 任务模块

### 1. Segmentation (牙齿分割)
- **目标**: 从口腔扫描中分割出单个牙齿
- **模型**: U-Net, SegFormer, PointNet++
- **输入**: 3D 点云或 2D 图像
- **输出**: 每个牙齿的分割掩码

### 2. Landmarks (地标点检测)
- **目标**: 检测牙齿关键点和解剖标志
- **模型**: HRNet, KeypointRCNN
- **输入**: 牙齿模型或图像
- **输出**: 关键点坐标

### 3. Tooth Axis (牙轴检测)
- **目标**: 自动检测牙齿的长轴方向
- **模型**: 回归网络, 3D CNN
- **输入**: 单个牙齿的 3D 模型
- **输出**: 牙轴向量和方向

### 4. Root Simulation (牙根模拟)
- **目标**: 从牙冠预测完整的牙根形态
- **模型**: GAN, VAE, Implicit Neural Representations
- **输入**: 牙冠 3D 模型
- **输出**: 完整的牙齿模型（含牙根）

### 5. Gingiva (牙龈处理)
- **目标**: 牙龈重建、分割和动画
- **模型**: Mesh generation networks, Deformation networks
- **输入**: 口腔扫描数据
- **输出**: 虚拟牙龈模型

### 6. Classification (分类任务)
- **目标**: 牙齿编号、角度分类等
- **模型**: ResNet, EfficientNet, Vision Transformer
- **输入**: 牙齿图像或特征
- **输出**: 分类标签

### 7. Reconstruction (3D 重建)
- **目标**: 近中面重建、牙冠修复等
- **模型**: Shape completion networks, Implicit functions
- **输入**: 不完整的 3D 数据
- **输出**: 完整的 3D 重建模型

## 快速开始

### 安装依赖

```bash
cd python
pip install -r requirements.txt
```

### 训练模型

以牙齿分割为例：

```bash
# 编辑配置文件
vim segmentation/config.yaml

# 开始训练
python segmentation/train.py --config segmentation/config.yaml

# 使用 GPU
python segmentation/train.py --config segmentation/config.yaml --gpu 0
```

### 推理预测

```bash
# 单个文件推理
python segmentation/inference.py --model checkpoints/seg_best.pth --input data/test_scan.obj

# 批量推理
python segmentation/inference.py --model checkpoints/seg_best.pth --input_dir data/test/ --output_dir results/
```

## 通用工具 (Common)

`common/` 文件夹包含所有任务共享的工具：

- **utils.py**: 数据加载、保存、转换等工具
- **metrics.py**: 评估指标（IoU, Dice, 准确率等）
- **visualization.py**: 结果可视化
- **base_trainer.py**: 通用训练框架
- **augmentation.py**: 数据增强

## 开发指南

### 添加新任务

1. 创建新的任务文件夹：
```bash
mkdir python/new_task
```

2. 创建必要的文件：
```
new_task/
├── train.py
├── inference.py
├── model.py
├── dataset.py
├── config.yaml
└── README.md
```

3. 继承通用基类：
```python
from common.base_trainer import BaseTrainer

class MyTaskTrainer(BaseTrainer):
    # 实现具体逻辑
    pass
```

### 代码规范

- 使用 Python 3.8+
- 遵循 PEP 8 代码风格
- 添加类型注解
- 编写文档字符串
- 添加单元测试

## 数据格式

### 3D 数据
- 支持格式: `.obj`, `.ply`, `.stl`
- 点云格式: numpy array (N, 3)
- 网格格式: vertices + faces

### 2D 数据
- 图像格式: `.png`, `.jpg`
- 分割掩码: 单通道图像，每个像素值代表类别

### 标注格式
- 分割标注: JSON 或二值掩码
- 关键点标注: JSON 格式存储坐标
- 分类标注: CSV 文件

## 模型权重

训练好的模型权重保存在 `checkpoints/` 目录：

```
checkpoints/
├── segmentation_best.pth
├── landmarks_v2.pth
├── tooth_axis_resnet50.pth
└── ...
```

## 性能基准

| 任务 | 模型 | 数据集 | 指标 | 分数 |
|------|------|--------|------|------|
| 分割 | U-Net | Internal | IoU | 92.3% |
| 地标 | HRNet | Internal | PCK@2mm | 95.1% |
| 分类 | ResNet-50 | Internal | Acc | 96.8% |

## 相关链接

- C++ 实现: [../src/](../src/)
- 项目文档: [../README.md](../README.md)
- 模型文档: [../models/README.md](../models/README.md)

## 许可证

与主项目相同
