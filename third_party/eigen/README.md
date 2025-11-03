# Eigen - 线性代数库

Eigen 是一个高性能的 C++ 模板库，用于线性代数、矩阵和向量运算、数值分析及相关算法。

## 📋 基本信息

- **官网**: https://eigen.tuxfamily.org/
- **版本**: 3.4.0+
- **许可证**: MPL2 (Mozilla Public License 2.0)
- **类型**: Header-only 库

## 🎯 在本项目中的应用

### 使用模块
1. **预处理模块**
   - PCA 主成分分析（自动调整颌平面）
   - 矩阵变换（坐标系转换）
   
2. **公共工具**
   - 几何计算（点、向量、矩阵运算）
   - 最小二乘拟合
   
3. **分析模块**
   - 特征提取
   - 曲线拟合

### 主要功能
- 矩阵和向量运算
- 线性方程求解
- 特征值分解
- SVD 分解
- 最小二乘拟合

## 🚀 安装

### Ubuntu/Debian
```bash
sudo apt-get install libeigen3-dev
```

### macOS
```bash
brew install eigen
```

### Windows (vcpkg)
```bash
vcpkg install eigen3
```

### 从源码编译
```bash
git clone https://gitlab.com/libeigen/eigen.git
cd eigen
mkdir build && cd build
cmake ..
sudo make install
```

## 🔧 CMake 集成

### 方式 1: 使用系统安装的 Eigen
```cmake
find_package(Eigen3 3.3 REQUIRED NO_MODULE)
target_link_libraries(your_target Eigen3::Eigen)
```

### 方式 2: 使用本地副本
如果将 Eigen 放在 `third_party/eigen/` 下：
```cmake
include_directories(${CMAKE_SOURCE_DIR}/third_party/eigen)
```

## 💡 使用示例

```cpp
#include <Eigen/Dense>
#include <iostream>

int main() {
  // 创建 3x3 矩阵
  Eigen::Matrix3d mat;
  mat << 1, 2, 3,
         4, 5, 6,
         7, 8, 9;
  
  // 创建向量
  Eigen::Vector3d vec(1, 2, 3);
  
  // 矩阵-向量乘法
  Eigen::Vector3d result = mat * vec;
  
  std::cout << "Result:\n" << result << std::endl;
  
  // PCA 示例
  Eigen::MatrixXd data(10, 3);
  // ... 填充数据 ...
  
  // 计算协方差矩阵
  Eigen::MatrixXd centered = data.rowwise() - data.colwise().mean();
  Eigen::MatrixXd cov = (centered.adjoint() * centered) / double(data.rows() - 1);
  
  // 特征值分解
  Eigen::SelfAdjointEigenSolver<Eigen::MatrixXd> eigen_solver(cov);
  Eigen::MatrixXd eigen_vectors = eigen_solver.eigenvectors();
  
  return 0;
}
```

## 📚 常用类型

- `Eigen::Vector3d` - 3D 双精度向量
- `Eigen::Matrix3d` - 3x3 双精度矩阵
- `Eigen::MatrixXd` - 动态大小双精度矩阵
- `Eigen::VectorXd` - 动态大小双精度向量

## ⚙️ 编译优化

Eigen 支持 SIMD 指令加速：
```cmake
# 启用 AVX
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mavx")

# 启用 AVX2
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mavx2")
```

## 🔗 相关资源

- [官方文档](https://eigen.tuxfamily.org/dox/)
- [快速参考指南](https://eigen.tuxfamily.org/dox/group__QuickRefPage.html)
- [教程](https://eigen.tuxfamily.org/dox/GettingStarted.html)

## ⚠️ 注意事项

1. Eigen 是 header-only 库，无需编译
2. 使用 `-O3` 优化可显著提升性能
3. 默认列主序存储（column-major）
4. 避免在循环中频繁创建临时对象

---

**状态**: ✅ 已配置
**最后检查**: 2025-11-03
