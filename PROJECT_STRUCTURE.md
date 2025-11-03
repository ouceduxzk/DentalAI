# 项目结构说明

## 完整目录树

```
/workspace/
├── CMakeLists.txt                    # 顶层CMake配置
├── README.md                         # 项目说明文档
├── TASK_MANAGEMENT.md                # 任务管理文档（1168行）
├── PROJECT_STRUCTURE.md              # 本文件
├── build.sh                          # 快速构建脚本
├── .clang-format                     # Google C++代码格式配置
├── .gitignore                        # Git忽略文件配置
│
├── src/                              # 源代码目录
│   ├── common/                       # 公共模块 (7个文件)
│   │   ├── CMakeLists.txt
│   │   ├── types.h                   # 通用数据类型定义
│   │   ├── types.cc
│   │   ├── mesh_utils.h              # 网格处理工具
│   │   ├── mesh_utils.cc
│   │   ├── geometry_utils.h          # 几何计算工具
│   │   └── geometry_utils.cc
│   │
│   ├── preprocessing/                # 牙颌预处理模块 (11个文件)
│   │   ├── CMakeLists.txt
│   │   ├── auto_adjust_plane.h       # 自动调整颌平面
│   │   ├── auto_adjust_plane.cc
│   │   ├── manual_adjust_plane.h     # 手动调整颌平面
│   │   ├── manual_adjust_plane.cc
│   │   ├── flying_edge_removal.h     # 飞边处理
│   │   ├── flying_edge_removal.cc
│   │   ├── bubble_repair.h           # 气泡修复
│   │   ├── bubble_repair.cc
│   │   ├── depression_repair.h       # 凹陷修复
│   │   └── depression_repair.cc
│   │
│   ├── segmentation/                 # 牙颌分割模块 (15个文件)
│   │   ├── CMakeLists.txt
│   │   ├── gingival_margin_drawing.h       # 牙颈线点画
│   │   ├── gingival_margin_drawing.cc
│   │   ├── tooth_contour_editing.h         # 牙齿轮廓编辑
│   │   ├── tooth_contour_editing.cc
│   │   ├── tooth_numbering.h               # 牙齿编号
│   │   ├── tooth_numbering.cc
│   │   ├── proximal_surface_segmentation.h # 邻面分割
│   │   ├── proximal_surface_segmentation.cc
│   │   ├── landmark_marking.h              # 标志点标记
│   │   ├── landmark_marking.cc
│   │   ├── auto_tooth_segmentation.h       # 自动牙齿分割（AI）
│   │   ├── auto_tooth_segmentation.cc
│   │   ├── auto_tooth_numbering.h          # 自动牙齿编号
│   │   └── auto_tooth_numbering.cc
│   │
│   ├── reconstruction/               # 牙齿重建模块 (15个文件)
│   │   ├── CMakeLists.txt
│   │   ├── auto_tooth_axis.h               # 自动牙轴生成
│   │   ├── auto_tooth_axis.cc
│   │   ├── manual_tooth_axis.h             # 手动调整牙轴
│   │   ├── manual_tooth_axis.cc
│   │   ├── auto_proximal_reconstruction.h  # 自动邻面重建
│   │   ├── auto_proximal_reconstruction.cc
│   │   ├── manual_proximal_reconstruction.h
│   │   ├── manual_proximal_reconstruction.cc
│   │   ├── crown_repair.h                  # 牙冠修复
│   │   ├── crown_repair.cc
│   │   ├── virtual_gingiva_reconstruction.h # 虚拟牙龈重建
│   │   ├── virtual_gingiva_reconstruction.cc
│   │   ├── root_simulation.h               # 牙根模拟
│   │   └── root_simulation.cc
│   │
│   ├── analysis/                     # 牙齿分析模块 (15个文件)
│   │   ├── CMakeLists.txt
│   │   ├── landmark_detection.h            # 特征点识别
│   │   ├── landmark_detection.cc
│   │   ├── ipr_simulation.h                # 邻面去釉模拟
│   │   ├── ipr_simulation.cc
│   │   ├── gingiva_animation.h             # 虚拟牙龈随动
│   │   ├── gingiva_animation.cc
│   │   ├── arch_curve_analysis.h           # 牙弓曲线分析
│   │   ├── arch_curve_analysis.cc
│   │   ├── spee_curve_analysis.h           # Spee曲线分析
│   │   ├── spee_curve_analysis.cc
│   │   ├── angle_classification.h          # 安氏分类
│   │   ├── angle_classification.cc
│   │   ├── overjet_overbite_analysis.h     # 覆合覆盖分析
│   │   └── overjet_overbite_analysis.cc
│   │
│   └── output/                       # 输出模块 (5个文件)
│       ├── CMakeLists.txt
│       ├── mesh_exporter.h                 # 三维牙齿输出
│       ├── mesh_exporter.cc
│       ├── mesh_with_gingiva_exporter.h    # 带牙龈输出
│       └── mesh_with_gingiva_exporter.cc
│
├── include/                          # 公共头文件目录
│
├── tests/                            # 测试目录 (6个文件)
│   ├── CMakeLists.txt
│   ├── test_main.cc
│   ├── test_mesh_utils.cc
│   ├── test_geometry_utils.cc
│   ├── test_preprocessing.cc
│   └── test_segmentation.cc
│
└── scripts/                          # Python辅助脚本目录
    ├── generate_remaining_files.sh
    └── generate_all_modules.sh

```

## 统计信息

- **总文件数**: 75+ 个文件
- **C++头文件(.h)**: 31个
- **C++源文件(.cc)**: 31个
- **CMakeLists.txt**: 7个
- **测试文件**: 5个
- **文档文件**: 4个

## 模块文件统计

| 模块 | 头文件 | 源文件 | 总计 |
|------|--------|--------|------|
| common | 3 | 3 | 6 |
| preprocessing | 5 | 5 | 10 |
| segmentation | 7 | 7 | 14 |
| reconstruction | 7 | 7 | 14 |
| analysis | 7 | 7 | 14 |
| output | 2 | 2 | 4 |
| tests | - | 5 | 5 |
| **总计** | **31** | **36** | **67** |

## 代码行数估算

- **公共模块**: ~1000行
- **预处理模块**: ~800行
- **分割模块**: ~1000行
- **重建模块**: ~700行
- **分析模块**: ~700行
- **输出模块**: ~400行
- **测试**: ~200行
- **总计**: ~4800行代码

## 命名规范

### 文件命名
- 小写 + 下划线: `auto_adjust_plane.h`
- 模块目录: 小写英文单词

### C++命名
- **类名**: `PascalCase` (例: `AutoAdjustPlane`)
- **函数名**: `PascalCase` (例: `Process()`)
- **变量名**: `snake_case` (例: `input_mesh`)
- **成员变量**: `snake_case_` (例: `config_`)
- **常量**: `kPascalCase` (例: `kMaxIterations`)
- **命名空间**: `lowercase` (例: `dental::preprocessing`)

### 头文件保护
格式: `SRC_MODULE_FILENAME_H_`
示例: `SRC_PREPROCESSING_AUTO_ADJUST_PLANE_H_`

## 快速导航

### 查找功能模块

**牙颌预处理**:
- 颌平面调整: `src/preprocessing/auto_adjust_plane.{h,cc}`
- 飞边处理: `src/preprocessing/flying_edge_removal.{h,cc}`
- 修复功能: `src/preprocessing/bubble_repair.{h,cc}`

**牙颌分割**:
- 牙颈线: `src/segmentation/gingival_margin_drawing.{h,cc}`
- 自动分割: `src/segmentation/auto_tooth_segmentation.{h,cc}`

**牙齿重建**:
- 牙轴生成: `src/reconstruction/auto_tooth_axis.{h,cc}`
- 邻面重建: `src/reconstruction/auto_proximal_reconstruction.{h,cc}`
- 牙龈重建: `src/reconstruction/virtual_gingiva_reconstruction.{h,cc}`

**牙齿分析**:
- 特征点: `src/analysis/landmark_detection.{h,cc}`
- 牙龈动画: `src/analysis/gingiva_animation.{h,cc}`

**输出**:
- Mesh导出: `src/output/mesh_exporter.{h,cc}`

## 构建流程

```bash
# 1. 配置
cmake -B build -DCMAKE_BUILD_TYPE=Release

# 2. 编译
cmake --build build -j$(nproc)

# 3. 测试
cd build && ctest

# 或使用快速构建脚本
./build.sh
```

## 依赖关系

```
output ─┐
        ├─> common
analysis─┤
        ├─> reconstruction ─┐
        │                   │
        ├─> segmentation ───┼─> common
        │                   │
        └─> preprocessing ──┘
```

