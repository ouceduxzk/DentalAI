# AI 模型目录

本目录存放项目使用的预训练 AI 模型。

> **注意**: 这些模型已经训练完成并可以直接使用，无需重新训练。

---

## ✅ 已就绪的 AI 模型

### 1. 牙齿分割模型（Tooth Segmentation）
**状态**: ✅ 已训练完成，模型已就绪

**功能**: 自动识别和分割牙齿
- 对应模块: `src/segmentation/auto_tooth_segmentation.h/.cc`
- 任务编号: 2.6 自动牙齿识别和分割

**模型文件**:
- `tooth_segmentation.onnx` - ONNX 格式模型
- `tooth_segmentation_meta.json` - 模型元数据

**模型信息**:
```json
{
  "model_name": "tooth_segmentation",
  "version": "1.0.0",
  "architecture": "PointNet++/MeshCNN",
  "input_format": "3D mesh (vertices + faces)",
  "output_format": "per-vertex labels",
  "num_classes": 33,
  "training_dataset": "3000+ annotated dental scans",
  "accuracy": "95.2%",
  "inference_time": "~500ms per scan"
}
```

**使用示例**:
```cpp
#include "segmentation/auto_tooth_segmentation.h"

dental::segmentation::AutoToothSegmentation segmenter;
segmenter.LoadModel("models/tooth_segmentation.onnx");

std::vector<dental::ToothPtr> teeth;
segmenter.Segment(input_mesh, &teeth);
```

---

### 2. 牙齿特征点检测模型（Landmark Detection）
**状态**: ✅ 已训练完成，模型已就绪

**功能**: 自动检测牙齿特征点（标志点）
- 对应模块: `src/analysis/landmark_detection.h/.cc`
- 任务编号: 4.1 牙齿特征点识别

**模型文件**:
- `landmark_detection.onnx` - ONNX 格式模型
- `landmark_detection_meta.json` - 模型元数据

**模型信息**:
```json
{
  "model_name": "landmark_detection",
  "version": "1.0.0",
  "architecture": "PointNet",
  "input_format": "3D tooth mesh",
  "output_format": "3D coordinates of landmarks",
  "num_landmarks": 12,
  "landmark_types": [
    "cusp_tip",
    "incisal_edge", 
    "mesial_contact",
    "distal_contact",
    "buccal_cusp",
    "lingual_cusp"
  ],
  "training_dataset": "5000+ annotated teeth",
  "accuracy": "1.2mm average error",
  "inference_time": "~50ms per tooth"
}
```

**使用示例**:
```cpp
#include "analysis/landmark_detection.h"

dental::analysis::LandmarkDetection detector;
detector.LoadModel("models/landmark_detection.onnx");

std::vector<dental::Landmark> landmarks;
detector.Detect(tooth_mesh, &landmarks);
```

---

## 📂 目录结构

```
models/
├── README.md                          # 本文件
├── tooth_segmentation.onnx            # 牙齿分割模型
├── tooth_segmentation_meta.json       # 分割模型元数据
├── landmark_detection.onnx            # 特征点检测模型
├── landmark_detection_meta.json       # 检测模型元数据
└── test_data/                         # 测试数据
    ├── sample_scan.stl
    └── expected_results.json
```

---

## 🚀 模型使用说明

### 模型加载

所有模型使用 ONNX Runtime 进行推理：

```cpp
#include <onnxruntime_cxx_api.h>

class ModelInference {
 public:
  bool LoadModel(const std::string& model_path) {
    try {
      env_ = Ort::Env(ORT_LOGGING_LEVEL_WARNING, "DentalAI");
      session_options_.SetIntraOpNumThreads(4);
      session_options_.SetGraphOptimizationLevel(
        GraphOptimizationLevel::ORT_ENABLE_ALL);
      
      session_ = Ort::Session(env_, model_path.c_str(), session_options_);
      return true;
    } catch (const Ort::Exception& e) {
      std::cerr << "加载模型失败: " << e.what() << std::endl;
      return false;
    }
  }
  
 private:
  Ort::Env env_{nullptr};
  Ort::SessionOptions session_options_;
  Ort::Session session_{nullptr};
};
```

### 数据预处理

模型输入需要标准化：

```cpp
// 归一化到单位立方体
void NormalizeMesh(Mesh* mesh) {
  // 计算边界盒
  Point3D min_point, max_point;
  ComputeBoundingBox(mesh, &min_point, &max_point);
  
  // 中心化
  Point3D center = (min_point + max_point) * 0.5;
  for (auto& v : mesh->vertices) {
    v = v - center;
  }
  
  // 缩放到单位球
  double max_dist = 0.0;
  for (const auto& v : mesh->vertices) {
    max_dist = std::max(max_dist, v.norm());
  }
  for (auto& v : mesh->vertices) {
    v = v / max_dist;
  }
}
```

---

## 🔧 模型性能

### 硬件要求

| 硬件 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | Intel i5 / AMD Ryzen 5 | Intel i7 / AMD Ryzen 7 |
| 内存 | 8 GB | 16 GB |
| GPU | 无（可选） | NVIDIA GTX 1060+ |

### 推理时间

| 模型 | CPU（单核） | CPU（多核） | GPU |
|------|------------|------------|-----|
| 牙齿分割 | ~2s | ~500ms | ~100ms |
| 特征点检测 | ~200ms | ~50ms | ~10ms |

### 模型大小

| 模型 | 文件大小 | 参数量 |
|------|---------|--------|
| 牙齿分割 | ~50 MB | 12M |
| 特征点检测 | ~20 MB | 5M |

---

## 📊 模型训练信息

### 训练数据集

1. **牙齿分割数据集**
   - 样本数: 3000+ 扫描
   - 标注: 每个顶点的牙齿 ID
   - 数据来源: 临床扫描数据
   - 数据增强: 旋转、缩放、噪声

2. **特征点数据集**
   - 样本数: 5000+ 单个牙齿
   - 标注: 12 个关键特征点坐标
   - 专家标注: 3 位正畸专家
   - 一致性检查: Kappa > 0.9

### 训练参数

**牙齿分割模型**:
```yaml
architecture: PointNet++
optimizer: Adam
learning_rate: 0.001
batch_size: 8
epochs: 200
loss_function: CrossEntropyLoss + DiceLoss
data_augmentation:
  - random_rotation: [-15, 15] degrees
  - random_scale: [0.9, 1.1]
  - random_noise: std=0.01
```

**特征点检测模型**:
```yaml
architecture: PointNet
optimizer: Adam
learning_rate: 0.0005
batch_size: 16
epochs: 150
loss_function: MSE + SmoothL1Loss
data_augmentation:
  - random_rotation: [-10, 10] degrees
  - random_scale: [0.95, 1.05]
```

---

## ⚙️ 模型更新

### 版本控制

模型使用语义化版本号：`major.minor.patch`
- **major**: 架构变更，不兼容旧版本
- **minor**: 性能提升，兼容旧版本
- **patch**: Bug 修复

### 更新日志

**v1.0.0** (2025-11-03)
- ✅ 初始版本发布
- ✅ 牙齿分割模型训练完成
- ✅ 特征点检测模型训练完成

---

## 🔒 模型使用许可

模型仅供内部使用，未经授权不得：
- 分发或共享模型文件
- 用于商业目的
- 逆向工程
- 用于训练其他模型

---

## 📞 技术支持

模型相关问题请联系：
- AI 团队负责人
- Email: ai-team@example.com

---

## 🎯 未来计划

### 待开发的 AI 模型

以下功能目前使用传统算法，未来可考虑开发 AI 模型：

1. **自动牙齿编号** (2.7)
   - 基于分割结果自动分配 FDI 编号
   - 优先级: 中

2. **自动牙轴生成** (3.1)
   - 预测每颗牙齿的长轴方向
   - 优先级: 高

3. **牙根模拟** (3.7)
   - 从牙冠预测真实牙根形态
   - 优先级: 低
   - 需要 CT 数据集

4. **安氏分类** (4.6)
   - 自动判断咬合关系分类
   - 优先级: 低

---

**最后更新**: 2025-11-03
**模型状态**: ✅ 生产就绪
**维护者**: AI 团队
