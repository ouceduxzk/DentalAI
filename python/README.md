# Python AI 算法模块

这个文件夹包含了所有与 Python 相关的 AI 算法实现，主要用于牙科模型的深度学习训练和测试。

## 目录结构

```
python/
├── ai_algorithms/          # AI 算法核心模块
│   ├── training/          # 训练相关代码
│   ├── testing/           # 测试和验证代码
│   ├── models/            # 模型定义和架构
│   ├── data/              # 数据处理和加载
│   └── utils/             # 工具函数和辅助代码
├── requirements.txt       # Python 依赖包
├── setup.py              # 安装配置
└── README.md             # 本文档
```

## 功能模块

### Training (训练)
- 模型训练脚本
- 训练配置管理
- 训练日志和可视化
- 模型检查点保存

### Testing (测试)
- 模型评估脚本
- 性能指标计算
- 测试结果可视化
- 推理和预测

### Models (模型)
- 深度学习模型架构
- 预训练模型
- 模型导出和转换

### Data (数据)
- 数据集加载器
- 数据预处理
- 数据增强
- 数据标注工具

### Utils (工具)
- 通用工具函数
- 配置文件解析
- 日志记录
- 可视化工具

## 安装依赖

```bash
cd python
pip install -r requirements.txt
```

## 使用示例

### 训练模型
```bash
python -m ai_algorithms.training.train --config configs/train_config.yaml
```

### 测试模型
```bash
python -m ai_algorithms.testing.test --model-path checkpoints/model_best.pth
```

## 开发指南

1. 所有新的 AI 算法应该添加到 `ai_algorithms/` 目录下
2. 训练脚本应放在 `training/` 目录
3. 测试和评估脚本应放在 `testing/` 目录
4. 共享的工具函数应放在 `utils/` 目录

## 相关链接

- 主项目 README: [../README.md](../README.md)
- 模型文档: [../models/README.md](../models/README.md)
