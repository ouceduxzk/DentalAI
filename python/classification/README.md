# 分类任务 (Classification)

## 任务描述

各种牙齿相关的分类任务。

## 任务列表

1. **牙齿编号**: 自动识别牙齿的 FDI 编号
2. **角度分类**: Angle 分类 (I 类、II 类、III 类)
3. **病理分类**: 龋齿、牙周病等检测
4. **牙齿类型**: 切牙、尖牙、前磨牙、磨牙

## 文件结构

```
classification/
├── tooth_numbering/
├── angle_classification/
├── pathology_detection/
└── README.md
```

## 使用方法

```bash
# 训练角度分类模型
python classification/angle_classification/train.py

# 推理
python classification/angle_classification/inference.py --model checkpoints/angle_cls.pth --input scan.obj
```
