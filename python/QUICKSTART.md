# Python AI 模块快速入门

## 安装

```bash
cd /workspace/python

# 安装基础依赖
pip install -r requirements.txt

# 或者使用 setup.py 安装
pip install -e .
```

## 目录结构总览

```
python/
├── segmentation/          # 牙齿分割
│   ├── train.py          # ✅ 训练脚本
│   ├── inference.py      # ✅ 推理脚本
│   ├── model.py          # ✅ 模型定义
│   ├── dataset.py        # ✅ 数据集
│   ├── config.yaml       # ✅ 配置文件
│   └── README.md         # ✅ 说明文档
│
├── landmarks/            # 地标点检测
│   ├── train.py          # ✅
│   ├── model.py          # ✅
│   ├── dataset.py        # ✅
│   ├── config.yaml       # ✅
│   └── README.md         # ✅
│
├── tooth_axis/           # 牙轴检测
│   ├── train.py          # ✅
│   ├── model.py          # ✅
│   ├── dataset.py        # ✅
│   ├── config.yaml       # ✅
│   └── README.md         # ✅
│
├── root_simulation/      # 牙根模拟
│   └── README.md         # ✅
│
├── gingiva/             # 牙龈处理
│   └── README.md         # ✅
│
├── classification/       # 分类任务
│   └── README.md         # ✅
│
├── reconstruction/       # 3D 重建
│   └── README.md         # ✅
│
└── common/              # 通用工具
    ├── base_trainer.py  # ✅ 基础训练器
    ├── utils.py         # ✅ 工具函数
    ├── metrics.py       # ✅ 评估指标
    └── __init__.py      # ✅
```

## 快速开始示例

### 1. 牙齿分割训练

```bash
# 编辑配置文件，设置数据路径
vim segmentation/config.yaml

# 开始训练
python segmentation/train.py --config segmentation/config.yaml

# 使用特定 GPU
python segmentation/train.py --config segmentation/config.yaml --gpus 0

# 从检查点继续训练
python segmentation/train.py --resume checkpoints/segmentation/checkpoint_epoch_50.pth
```

### 2. 牙齿分割推理

```bash
# 单个文件推理
python segmentation/inference.py \
    --model checkpoints/segmentation/best_model.pth \
    --input data/test_scan.obj \
    --output results/segmented.obj

# 批量推理
python segmentation/inference.py \
    --model checkpoints/segmentation/best_model.pth \
    --input_dir data/test/ \
    --output_dir results/

# 带可视化
python segmentation/inference.py \
    --model checkpoints/segmentation/best_model.pth \
    --input data/test_scan.obj \
    --visualize
```

### 3. 地标点检测

```bash
# 训练
python landmarks/train.py --config landmarks/config.yaml

# 推理（会生成 landmarks.json）
python landmarks/inference.py \
    --model checkpoints/landmarks/best.pth \
    --input tooth.obj \
    --output landmarks.json
```

### 4. 牙轴检测

```bash
# 训练
python tooth_axis/train.py --config tooth_axis/config.yaml

# 推理
python tooth_axis/inference.py \
    --model checkpoints/tooth_axis/best.pth \
    --input tooth.obj
```

## 数据准备

### 分割任务数据结构

```
data/segmentation/
├── train/
│   ├── scans/
│   │   ├── case001.obj
│   │   ├── case002.obj
│   │   └── ...
│   └── labels/
│       ├── case001.json
│       ├── case002.json
│       └── ...
├── val/
│   ├── scans/
│   └── labels/
└── test/
    ├── scans/
    └── labels/
```

### 标签格式示例

**分割标签** (`labels/case001.json`):
```json
{
  "filename": "case001.obj",
  "num_points": 50000,
  "labels": [0, 0, 1, 1, 1, ..., 16, 16, 16],
  "tooth_ids": [11, 12, 13, 14, 15, 16, ...]
}
```

**地标点标签** (`landmarks/case001.json`):
```json
{
  "filename": "tooth_11.obj",
  "landmarks": [
    [10.5, 20.3, 15.8],
    [12.1, 22.5, 16.2],
    ...
  ],
  "landmark_names": ["cusp", "cervical_buccal", "cervical_lingual"]
}
```

**牙轴标签** (`axes/tooth_11.json`):
```json
{
  "filename": "tooth_11.obj",
  "origin": [10.5, 20.3, 15.8],
  "direction": [0.1, 0.2, 0.97],
  "tooth_id": 11
}
```

## 使用通用工具

```python
import sys
sys.path.append('/workspace/python')

from common.utils import load_mesh, save_mesh, normalize_points
from common.metrics import segmentation_metrics, landmark_metrics
from common.base_trainer import BaseTrainer

# 加载网格
vertices, faces = load_mesh('tooth.obj')

# 归一化点云
normalized_points = normalize_points(vertices)

# 计算分割指标
metrics = segmentation_metrics(pred_labels, gt_labels, num_classes=33)
print(f"Mean IoU: {metrics['mean_iou']:.4f}")
```

## 自定义训练器

```python
from common.base_trainer import BaseTrainer
import torch.nn as nn

class MyTaskTrainer(BaseTrainer):
    def _compute_loss(self, batch_data):
        # 自定义损失计算
        points, labels = batch_data
        outputs = self.model(points)
        loss = self.criterion(outputs, labels)
        return loss

# 使用自定义训练器
trainer = MyTaskTrainer(
    model=model,
    train_loader=train_loader,
    val_loader=val_loader,
    criterion=nn.CrossEntropyLoss(),
    optimizer=optimizer,
    scheduler=scheduler,
    device=device,
    config=config
)

trainer.train(epochs=100, save_dir='checkpoints/my_task')
```

## 配置文件说明

每个任务的 `config.yaml` 包含：

- **data**: 数据路径和参数
- **model**: 模型架构和超参数
- **training**: 训练相关配置（batch size, epochs, learning rate等）
- **loss**: 损失函数配置
- **evaluation**: 评估指标配置

## 添加新任务

1. 创建任务文件夹:
```bash
mkdir python/new_task
```

2. 创建必要文件:
```bash
touch python/new_task/{train.py,inference.py,model.py,dataset.py,config.yaml,README.md,__init__.py}
```

3. 实现核心功能:
   - `model.py`: 定义模型
   - `dataset.py`: 定义数据集
   - `train.py`: 继承 `BaseTrainer` 实现训练
   - `inference.py`: 实现推理逻辑
   - `config.yaml`: 配置参数

## 常见问题

### Q: 如何使用多 GPU 训练？
```bash
python segmentation/train.py --config segmentation/config.yaml --gpus 0,1,2,3
```

### Q: 如何可视化训练过程？
使用 TensorBoard:
```bash
tensorboard --logdir logs/
```

### Q: 如何导出模型为 ONNX？
```python
import torch

model.eval()
dummy_input = torch.randn(1, 10000, 3).cuda()
torch.onnx.export(model, dummy_input, "model.onnx")
```

### Q: 如何处理内存不足？
- 减小 batch_size
- 减少采样点数 num_points
- 使用梯度累积
- 使用混合精度训练

## 性能优化建议

1. **数据加载**: 使用 `num_workers=4` 并行加载
2. **混合精度**: 使用 `torch.cuda.amp` 加速训练
3. **模型量化**: 使用 `torch.quantization` 减小模型大小
4. **批量推理**: 处理多个样本时使用 batch inference

## 下一步

- 查看各个任务的 README.md 了解详细信息
- 准备你的数据集
- 修改配置文件
- 开始训练！

## 联系和贡献

如有问题或建议，欢迎提 Issue 或 PR。
