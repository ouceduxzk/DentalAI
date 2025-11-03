# 牙根模拟 (Root Simulation)

## 任务描述

从牙冠的 3D 模型预测和生成完整的牙齿模型（包括牙根）。

## 方法

- **基于学习的方法**: 使用 GAN、VAE 或隐式神经表示
- **基于统计的方法**: Shape completion using statistical models
- **混合方法**: 结合深度学习和几何约束

## 文件结构

```
root_simulation/
├── train.py          # GAN/VAE 训练
├── inference.py      # 牙根生成
├── model.py          # 生成器和判别器
├── dataset.py        # 牙冠-牙根配对数据
└── config.yaml       # 配置文件
```

## 使用方法

```bash
# 训练
python root_simulation/train.py --config root_simulation/config.yaml

# 生成牙根
python root_simulation/inference.py --model checkpoints/root_gen.pth --input crown.obj --output full_tooth.obj
```
