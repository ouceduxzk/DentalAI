# 第三方依赖库

本目录包含项目所需的第三方依赖库配置和说明。

> **注意**: AI 相关的库（如 ONNX Runtime）不包含在此处，因为项目已使用预训练的 AI 模型。

---

## 📦 核心依赖库

### 1. Eigen (v3.3+)
**用途**: 线性代数、矩阵运算
**许可证**: MPL2
**模块使用**:
- 预处理模块（PCA、坐标系变换）
- 几何工具（向量计算、矩阵运算）

### 2. CGAL (Computational Geometry Algorithms Library)
**用途**: 计算几何算法（补洞、网格修复、重建）
**许可证**: GPL/LGPL/Commercial
**模块使用**:
- 预处理模块（飞边处理、网格修复）
- 重建模块（补洞、refine算法）
- 牙冠修复

### 3. VCGlib (Visualization and Computer Graphics Library)
**用途**: 网格处理和操作
**许可证**: GPL
**模块使用**:
- 公共模块（网格工具）
- 预处理模块（网格修复、平滑）
- 输出模块（格式转换）

### 4. VTK (Visualization Toolkit)
**用途**: 3D可视化、数据处理
**许可证**: BSD
**模块使用**:
- 可视化预览
- 网格渲染
- 数据导出

### 5. PCL (Point Cloud Library) - 可选
**用途**: 点云处理
**许可证**: BSD
**模块使用**:
- 预处理模块（点云滤波）
- 特征提取

### 6. nlohmann/json (v3.x)
**用途**: JSON 配置文件解析
**许可证**: MIT
**模块使用**:
- 配置文件读写
- 参数管理
- 数据序列化

### 7. Google Test (v1.10+)
**用途**: C++ 单元测试框架
**许可证**: BSD
**模块使用**:
- 测试模块

### 8. Qt5 (可选)
**用途**: GUI 界面开发
**许可证**: LGPL/Commercial
**模块使用**:
- 手动调整功能
- 交互式编辑工具

---

## 🚀 快速安装

### Ubuntu/Debian
```bash
# 安装核心依赖
sudo apt-get update
sudo apt-get install -y \
    libeigen3-dev \
    libcgal-dev \
    libvtk9-dev \
    libgtest-dev \
    nlohmann-json3-dev

# 可选依赖
sudo apt-get install -y \
    libpcl-dev \
    qtbase5-dev \
    qttools5-dev
```

### macOS (使用 Homebrew)
```bash
brew install eigen cgal vtk googletest nlohmann-json

# 可选
brew install pcl qt@5
```

### Windows (使用 vcpkg)
```bash
vcpkg install eigen3 cgal vtk gtest nlohmann-json

# 可选
vcpkg install pcl qt5
```

---

## 📁 目录结构

```
third_party/
├── README.md                 # 本文件
├── eigen/                    # Eigen 配置
│   ├── README.md
│   └── FindEigen3.cmake
├── cgal/                     # CGAL 配置
│   ├── README.md
│   └── FindCGAL.cmake
├── vcglib/                   # VCGlib 源码或配置
│   ├── README.md
│   └── CMakeLists.txt
├── vtk/                      # VTK 配置
│   └── README.md
├── json/                     # nlohmann/json
│   ├── README.md
│   └── json.hpp (header-only)
├── googletest/               # Google Test
│   └── README.md
└── cmake/                    # CMake 查找脚本
    ├── FindVCG.cmake
    └── FindNlohmannJson.cmake
```

---

## 🔧 CMake 集成

在项目的 `CMakeLists.txt` 中，这些库已经通过以下方式集成：

```cmake
# 设置 CMake 模块路径
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/third_party/cmake")

# 查找核心依赖
find_package(Eigen3 3.3 REQUIRED)
find_package(CGAL REQUIRED)
find_package(VTK REQUIRED)
find_package(GTest REQUIRED)

# 可选依赖
find_package(PCL QUIET)
find_package(Qt5 COMPONENTS Core Widgets OpenGL QUIET)
```

---

## 📝 各库的详细说明

请查看各子目录下的 README.md 获取详细的安装、配置和使用说明。

---

## ⚠️ AI 模型相关说明

**本项目不包含 AI 推理引擎的第三方库（如 ONNX Runtime）**，原因如下：

1. **牙齿分割**（Auto Tooth Segmentation）- 已有预训练模型
2. **牙齿特征点检测**（Landmark Detection）- 已有预训练模型

这些功能使用的 AI 模型已经训练完成并部署，模型文件存储在独立的 `models/` 目录中。

如果将来需要重新训练或更新模型，可以使用以下工具（在开发环境中）：
- TensorFlow / PyTorch（模型训练）
- ONNX（模型转换）
- ONNX Runtime（模型推理，仅开发时需要）

---

## 🔄 更新依赖

建议定期检查并更新依赖库版本以获得性能提升和 bug 修复：

```bash
# Ubuntu
sudo apt-get update && sudo apt-get upgrade

# macOS
brew update && brew upgrade

# vcpkg
vcpkg upgrade
```

---

## 📊 版本兼容性

| 库名称 | 最低版本 | 推荐版本 | 测试版本 |
|--------|---------|---------|---------|
| Eigen | 3.3.0 | 3.4.0 | 3.4.0 |
| CGAL | 5.0 | 5.6 | 5.6 |
| VTK | 8.2 | 9.2 | 9.2 |
| GTest | 1.10 | 1.14 | 1.14 |
| nlohmann/json | 3.7 | 3.11 | 3.11 |
| PCL (可选) | 1.10 | 1.13 | 1.13 |
| Qt5 (可选) | 5.12 | 5.15 | 5.15 |

---

## 🐛 常见问题

### 1. CGAL 编译错误
确保安装了 GMP 和 MPFR：
```bash
sudo apt-get install libgmp-dev libmpfr-dev
```

### 2. VTK 找不到
手动指定 VTK 目录：
```bash
cmake -DVTK_DIR=/usr/local/lib/cmake/vtk-9.2 ..
```

### 3. Eigen 版本过旧
从源码编译最新版本：
```bash
git clone https://gitlab.com/libeigen/eigen.git
cd eigen && mkdir build && cd build
cmake .. && sudo make install
```

---

## 📞 技术支持

如有依赖库相关问题，请：
1. 查看对应子目录的 README.md
2. 访问官方文档
3. 提交 Issue

---

**最后更新**: 2025-11-03
**维护者**: 开发团队
