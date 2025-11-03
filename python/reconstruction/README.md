# 3D 重建 (Reconstruction)

## 任务描述

3D 牙齿模型的重建和修复。

## 任务列表

1. **近中面重建**: 自动重建牙齿的接触面
2. **牙冠修复**: 修复缺损的牙冠
3. **形状补全**: 从不完整的扫描重建完整模型

## 技术方法

- **Shape Completion Networks**
- **Implicit Neural Representations (INR)**
- **Point Cloud Completion**
- **Mesh Inpainting**

## 文件结构

```
reconstruction/
├── proximal_surface/    # 近中面重建
├── crown_repair/        # 牙冠修复
├── shape_completion/    # 形状补全
└── README.md
```

## 使用方法

```bash
# 训练形状补全模型
python reconstruction/shape_completion/train.py

# 推理
python reconstruction/shape_completion/inference.py --model checkpoints/completion.pth --input incomplete.obj --output complete.obj
```
