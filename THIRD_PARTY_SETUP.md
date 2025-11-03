# 第三方依赖库安装指南

本文档提供完整的第三方依赖库安装和配置指南。

---

## 📦 快速安装（推荐）

### Ubuntu/Debian

```bash
#!/bin/bash
# 完整的依赖安装脚本

# 更新包管理器
sudo apt-get update

# ===== 必需的依赖 =====
echo "安装必需的依赖库..."

# Eigen3 - 线性代数
sudo apt-get install -y libeigen3-dev

# CGAL - 计算几何
sudo apt-get install -y libcgal-dev libgmp-dev libmpfr-dev

# Boost（CGAL 依赖）
sudo apt-get install -y libboost-all-dev

# ===== 可选的依赖 =====
echo "安装可选的依赖库..."

# VTK - 可视化
sudo apt-get install -y libvtk9-dev

# PCL - 点云处理（可选）
sudo apt-get install -y libpcl-dev

# Qt5 - GUI（可选）
sudo apt-get install -y qtbase5-dev qttools5-dev libqt5opengl5-dev

# nlohmann/json
sudo apt-get install -y nlohmann-json3-dev

# Google Test
sudo apt-get install -y libgtest-dev
cd /usr/src/gtest
sudo cmake .
sudo make
sudo cp lib/*.a /usr/lib
cd -

echo "✅ 依赖安装完成！"
```

保存为 `install_dependencies.sh` 并运行：
```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### macOS

```bash
#!/bin/bash
# macOS 依赖安装脚本（使用 Homebrew）

# 安装 Homebrew（如果没有）
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 必需依赖
brew install eigen cgal boost

# 可选依赖
brew install vtk pcl qt@5 nlohmann-json googletest

echo "✅ 依赖安装完成！"
```

### Windows (vcpkg)

```powershell
# Windows 依赖安装脚本

# 安装 vcpkg（如果没有）
# git clone https://github.com/Microsoft/vcpkg.git
# cd vcpkg
# .\bootstrap-vcpkg.bat

# 必需依赖
.\vcpkg install eigen3:x64-windows
.\vcpkg install cgal:x64-windows

# 可选依赖
.\vcpkg install vtk:x64-windows
.\vcpkg install pcl:x64-windows
.\vcpkg install qt5:x64-windows
.\vcpkg install nlohmann-json:x64-windows
.\vcpkg install gtest:x64-windows

# 集成到 CMake
.\vcpkg integrate install
```

---

## 🔧 手动安装（特定库）

### 1. VCGlib（网格处理库）

VCGlib 不在系统包管理器中，需要手动克隆：

```bash
cd /workspace/third_party
git clone https://github.com/cnr-isti-vclab/vcglib.git

# 验证
ls vcglib/vcg/complex/complex.h
```

### 2. nlohmann/json（如果系统没有）

```bash
cd /workspace/third_party/json
wget https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp
```

或者使用 CMake FetchContent（已在项目中配置）。

---

## ✅ 验证安装

### 检查依赖是否正确安装

创建测试文件 `test_dependencies.cpp`：

```cpp
#include <Eigen/Dense>
#include <CGAL/Simple_cartesian.h>
#include <iostream>

int main() {
  // 测试 Eigen
  Eigen::Vector3d v(1, 2, 3);
  std::cout << "Eigen works: " << v.transpose() << std::endl;
  
  // 测试 CGAL
  typedef CGAL::Simple_cartesian<double> K;
  K::Point_3 p(1, 2, 3);
  std::cout << "CGAL works: " << p << std::endl;
  
  std::cout << "✅ All dependencies OK!" << std::endl;
  return 0;
}
```

编译并运行：
```bash
g++ -std=c++17 test_dependencies.cpp -o test_deps \
    -I/usr/include/eigen3 \
    -lCGAL -lgmp -lmpfr

./test_deps
```

### CMake 配置测试

```bash
cd /workspace
mkdir build && cd build
cmake ..

# 查看配置摘要，应该显示：
# ✅ Eigen3: 3.x.x
# ✅ CGAL: 5.x
# ✅ VCGlib: Found (或提示克隆)
# ✅ nlohmann/json: Found
# 等等
```

---

## 📚 各库的详细文档

每个第三方库都有详细的 README 文档：

- `third_party/eigen/README.md` - Eigen 使用说明
- `third_party/cgal/README.md` - CGAL 使用说明
- `third_party/vcglib/README.md` - VCGlib 使用说明
- `third_party/vtk/README.md` - VTK 使用说明
- `third_party/json/README.md` - nlohmann/json 使用说明
- `third_party/googletest/README.md` - Google Test 使用说明

---

## 🐛 常见问题

### 问题 1: CGAL 找不到 GMP

**错误信息**:
```
CMake Error: Could not find GMP
```

**解决方案**:
```bash
sudo apt-get install libgmp-dev libmpfr-dev
```

### 问题 2: VCGlib 头文件找不到

**错误信息**:
```
fatal error: vcg/complex/complex.h: No such file or directory
```

**解决方案**:
```bash
cd /workspace/third_party
git clone https://github.com/cnr-isti-vclab/vcglib.git
```

### 问题 3: Eigen 版本过旧

**错误信息**:
```
CMake Error: Eigen3 version 3.3 or higher required
```

**解决方案**:
```bash
# 从源码安装最新版
git clone https://gitlab.com/libeigen/eigen.git
cd eigen && mkdir build && cd build
cmake .. && sudo make install
```

### 问题 4: Qt5 找不到

**解决方案**:
```bash
# Ubuntu
sudo apt-get install qtbase5-dev

# macOS
brew install qt@5
export CMAKE_PREFIX_PATH="/usr/local/opt/qt@5:$CMAKE_PREFIX_PATH"
```

### 问题 5: VTK 版本不兼容

**解决方案**:
```bash
# 指定 VTK 路径
cmake -DVTK_DIR=/usr/local/lib/cmake/vtk-9.2 ..
```

---

## 📊 依赖关系图

```
项目模块依赖关系：

output ──────┐
             ├──> common ──> Eigen, nlohmann/json
analysis ────┤
             ├──> reconstruction ──> CGAL, VCGlib
             │
             ├──> segmentation ──> Eigen, CGAL
             │
             └──> preprocessing ──> CGAL, VCGlib, Eigen

可视化（可选）: VTK, Qt5
测试: Google Test
```

---

## 🔄 更新依赖

定期更新依赖以获得性能提升和 bug 修复：

### Ubuntu
```bash
sudo apt-get update
sudo apt-get upgrade
```

### macOS
```bash
brew update
brew upgrade
```

### vcpkg
```bash
cd vcpkg
git pull
.\vcpkg upgrade
```

---

## 📝 版本兼容性矩阵

| 依赖库 | 最低版本 | 推荐版本 | 测试版本 | 状态 |
|--------|---------|---------|---------|------|
| Eigen | 3.3.0 | 3.4.0 | 3.4.0 | ✅ 必需 |
| CGAL | 5.0 | 5.6 | 5.6 | ✅ 必需 |
| VCGlib | 2022.02 | latest | 2024.x | ⚠️ 需手动克隆 |
| VTK | 8.2 | 9.2 | 9.2 | 🔵 可选 |
| PCL | 1.10 | 1.13 | 1.13 | 🔵 可选 |
| Qt5 | 5.12 | 5.15 | 5.15 | 🔵 可选 |
| nlohmann/json | 3.7 | 3.11 | 3.11 | ✅ 已包含 |
| Google Test | 1.10 | 1.14 | 1.14 | 🔵 可选 |

---

## 💡 最小化安装

如果只想快速开始开发，只安装必需的依赖：

```bash
# 仅必需依赖
sudo apt-get install -y \
  libeigen3-dev \
  libcgal-dev \
  libgmp-dev \
  libmpfr-dev \
  libboost-all-dev

# 克隆 VCGlib
cd /workspace/third_party
git clone https://github.com/cnr-isti-vclab/vcglib.git

# nlohmann/json 已包含在项目中
```

这样就可以开始开发了。可视化和 GUI 功能暂时不可用，但不影响核心算法开发。

---

## 📞 获取帮助

如果遇到依赖安装问题：

1. 查看对应库的 `third_party/<库名>/README.md`
2. 查看官方文档
3. 提交 Issue 并附上：
   - 操作系统和版本
   - CMake 输出日志
   - 错误信息

---

**最后更新**: 2025-11-03
**维护者**: 开发团队

---

## 🎯 下一步

依赖安装完成后：

1. ✅ 验证安装: `cd build && cmake ..`
2. ✅ 编译项目: `cmake --build . -j$(nproc)`
3. ✅ 运行测试: `ctest`
4. 📖 开始开发: 查看 `README.md` 了解项目结构

Good luck! 🚀
