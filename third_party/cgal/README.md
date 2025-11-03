# CGAL - 计算几何算法库

CGAL (Computational Geometry Algorithms Library) 是一个强大的 C++ 库，提供高效可靠的几何算法。

## 📋 基本信息

- **官网**: https://www.cgal.org/
- **版本**: 5.0+
- **许可证**: GPL/LGPL/Commercial（三重许可）
- **类型**: 编译库

## 🎯 在本项目中的应用

### 使用模块

1. **预处理模块**
   - 网格修复（飞边处理）
   - 连通域分析
   - 非流形边检测和修复
   
2. **重建模块**
   - 网格补洞（Hole Filling）
   - 网格细化（Refinement）
   - 牙冠修复
   - 邻面重建
   
3. **公共工具**
   - 网格拓扑检查
   - 网格质量优化

### 主要功能

- **网格处理**
  - 网格补洞
  - 网格简化
  - 网格细化
  - 网格布尔运算
  
- **几何算法**
  - Delaunay 三角化
  - 凸包计算
  - 最短路径
  - 碰撞检测

## 🚀 安装

### Ubuntu/Debian
```bash
# 安装 CGAL 及其依赖
sudo apt-get install libcgal-dev

# 安装必要的数学库
sudo apt-get install libgmp-dev libmpfr-dev libboost-all-dev
```

### macOS
```bash
brew install cgal
brew install gmp mpfr boost
```

### Windows (vcpkg)
```bash
vcpkg install cgal
```

### 从源码编译
```bash
# 下载源码
wget https://github.com/CGAL/cgal/releases/download/v5.6/CGAL-5.6.tar.xz
tar xf CGAL-5.6.tar.xz
cd CGAL-5.6

# 编译安装
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make
sudo make install
```

## 🔧 CMake 集成

```cmake
# 查找 CGAL
find_package(CGAL REQUIRED COMPONENTS Core)

# 链接 CGAL
target_link_libraries(your_target CGAL::CGAL)

# 如果使用 Qt（CGAL 可视化）
find_package(Qt5 COMPONENTS Widgets OpenGL)
target_link_libraries(your_target CGAL::CGAL_Qt5)
```

## 💡 使用示例

### 网格补洞
```cpp
#include <CGAL/Simple_cartesian.h>
#include <CGAL/Surface_mesh.h>
#include <CGAL/Polygon_mesh_processing/triangulate_hole.h>

typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_3 Point;
typedef CGAL::Surface_mesh<Point> Mesh;

void fill_hole(Mesh& mesh) {
  // 检测孔洞
  std::vector<halfedge_descriptor> border_cycles;
  CGAL::Polygon_mesh_processing::extract_boundary_cycles(mesh, 
    std::back_inserter(border_cycles));
  
  // 填充每个孔洞
  for(halfedge_descriptor h : border_cycles) {
    CGAL::Polygon_mesh_processing::triangulate_hole(mesh, h);
  }
}
```

### 网格细化
```cpp
#include <CGAL/Polygon_mesh_processing/refine.h>

void refine_mesh(Mesh& mesh) {
  // 细化网格
  CGAL::Polygon_mesh_processing::refine(
    mesh,
    faces(mesh),
    CGAL::parameters::density_control_factor(2.0)
  );
}
```

### 网格修复
```cpp
#include <CGAL/Polygon_mesh_processing/repair.h>

void repair_mesh(Mesh& mesh) {
  // 删除退化面
  CGAL::Polygon_mesh_processing::remove_degenerate_faces(mesh);
  
  // 删除孤立点
  CGAL::Polygon_mesh_processing::remove_isolated_vertices(mesh);
  
  // 缝合边界
  CGAL::Polygon_mesh_processing::stitch_borders(mesh);
}
```

### 碰撞检测
```cpp
#include <CGAL/Polygon_mesh_processing/collision_detection.h>

bool check_collision(const Mesh& mesh1, const Mesh& mesh2) {
  return CGAL::Polygon_mesh_processing::do_intersect(mesh1, mesh2);
}
```

## 📚 项目中使用的 CGAL 模块

| 功能 | CGAL 模块 | 对应的项目模块 |
|------|-----------|----------------|
| 补洞 | Hole Filling | 牙冠修复 |
| 网格细化 | Refinement | 虚拟牙龈重建 |
| 拓扑修复 | Repair | 飞边处理 |
| 布尔运算 | Boolean Operations | 邻面重建 |
| 最短路径 | Shortest Paths | 牙颈线点画 |

## ⚙️ 性能优化

```cmake
# 启用并行化
find_package(TBB)
if(TBB_FOUND)
  target_link_libraries(your_target TBB::tbb)
  add_definitions(-DCGAL_LINKED_WITH_TBB)
endif()

# Release 模式
set(CMAKE_BUILD_TYPE Release)
```

## 🔗 相关资源

- [官方文档](https://doc.cgal.org/)
- [网格处理手册](https://doc.cgal.org/latest/Polygon_mesh_processing/index.html)
- [示例代码](https://github.com/CGAL/cgal/tree/master/Polygon_mesh_processing/examples)
- [常见问题](https://www.cgal.org/FAQ.html)

## ⚠️ 注意事项

1. **许可证**: CGAL 使用 GPL/LGPL，商业项目需购买商业许可
2. **编译时间**: CGAL 使用大量模板，编译时间较长
3. **依赖**: 需要 GMP、MPFR、Boost 等依赖
4. **精度**: CGAL 提供精确计算，但可能影响性能

## 🐛 常见问题

### 1. 找不到 CGAL
```bash
# 手动指定路径
cmake -DCGAL_DIR=/usr/local/lib/cmake/CGAL ..
```

### 2. 链接错误
```cmake
# 添加依赖库
target_link_libraries(your_target 
  CGAL::CGAL 
  gmp 
  mpfr
)
```

### 3. 编译过慢
```bash
# 使用预编译头文件
target_precompile_headers(your_target PRIVATE <CGAL/...>)

# 使用 ccache
export CXX="ccache g++"
```

---

**状态**: ✅ 已配置
**最后检查**: 2025-11-03
