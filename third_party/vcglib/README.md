# VCGlib - 网格处理库

VCGlib 是一个 C++ 开源库，专门用于三角网格的处理、编辑和渲染。由意大利 ISTI-CNR 开发。

## 📋 基本信息

- **官网**: http://www.vcglib.net/
- **GitHub**: https://github.com/cnr-isti-vclab/vcglib
- **版本**: 2022.02+
- **许可证**: GPL v3
- **类型**: Header-only 库

## 🎯 在本项目中的应用

### 使用模块

1. **预处理模块**
   - 飞边处理
   - 网格平滑（Laplace、Taubin）
   - 网格简化
   
2. **公共工具**
   - 网格 I/O（STL、OBJ、PLY 等）
   - 网格拓扑操作
   - 网格质量评估
   
3. **重建模块**
   - 网格修复
   - 网格重建

### 主要功能

- **网格处理**
  - 网格平滑和去噪
  - 网格简化和细化
  - 网格采样
  - 法向计算
  
- **网格修复**
  - 非流形边修复
  - 退化面删除
  - 重复顶点合并
  
- **网格分析**
  - 曲率计算
  - 边界检测
  - 连通域分析

## 🚀 安装

### 方式 1: Git 子模块（推荐）
```bash
cd /workspace/third_party
git clone https://github.com/cnr-isti-vclab/vcglib.git
```

### 方式 2: 下载源码
```bash
wget https://github.com/cnr-isti-vclab/vcglib/archive/refs/heads/main.zip
unzip main.zip -d vcglib
```

### Ubuntu 依赖
```bash
# VCGlib 是 header-only，但示例需要以下依赖
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev
```

## 🔧 CMake 集成

```cmake
# 添加 VCGlib 头文件路径
include_directories(${CMAKE_SOURCE_DIR}/third_party/vcglib)

# VCGlib 是 header-only，无需链接
# 但需要链接数学库
target_link_libraries(your_target m)
```

## 💡 使用示例

### 加载和保存网格
```cpp
#include <vcg/complex/complex.h>
#include <vcg/complex/algorithms/update/bounding.h>
#include <wrap/io_trimesh/import.h>
#include <wrap/io_trimesh/export.h>

class MyVertex;
class MyEdge;
class MyFace;

struct MyUsedTypes : public vcg::UsedTypes<
  vcg::Use<MyVertex>::AsVertexType,
  vcg::Use<MyEdge>::AsEdgeType,
  vcg::Use<MyFace>::AsFaceType>{};

class MyVertex : public vcg::Vertex<MyUsedTypes, 
  vcg::vertex::Coord3f, vcg::vertex::Normal3f, vcg::vertex::BitFlags> {};
class MyFace   : public vcg::Face<MyUsedTypes, 
  vcg::face::VertexRef, vcg::face::Normal3f, vcg::face::BitFlags> {};
class MyEdge   : public vcg::Edge<MyUsedTypes> {};

class MyMesh : public vcg::tri::TriMesh<std::vector<MyVertex>, std::vector<MyFace>> {};

void load_and_save() {
  MyMesh mesh;
  
  // 加载 STL
  int result = vcg::tri::io::ImporterSTL<MyMesh>::Open(mesh, "input.stl");
  if(result != 0) {
    std::cerr << "加载失败" << std::endl;
    return;
  }
  
  // 更新边界盒
  vcg::tri::UpdateBounding<MyMesh>::Box(mesh);
  
  // 导出 PLY
  vcg::tri::io::ExporterPLY<MyMesh>::Save(mesh, "output.ply");
}
```

### Laplace 平滑
```cpp
#include <vcg/complex/algorithms/smooth.h>

void smooth_mesh(MyMesh& mesh, int iterations = 10) {
  // 更新拓扑
  vcg::tri::UpdateTopology<MyMesh>::FaceFace(mesh);
  vcg::tri::UpdateNormal<MyMesh>::PerVertexNormalizedPerFace(mesh);
  
  // Laplace 平滑
  vcg::tri::Smooth<MyMesh>::VertexCoordLaplacian(mesh, iterations);
  
  // 更新法向
  vcg::tri::UpdateNormal<MyMesh>::PerVertexNormalizedPerFace(mesh);
}
```

### 网格修复
```cpp
#include <vcg/complex/algorithms/clean.h>

void clean_mesh(MyMesh& mesh) {
  // 删除重复顶点
  int dup = vcg::tri::Clean<MyMesh>::RemoveDuplicateVertex(mesh);
  
  // 删除未引用的顶点
  int unref = vcg::tri::Clean<MyMesh>::RemoveUnreferencedVertex(mesh);
  
  // 删除退化面
  int degen = vcg::tri::Clean<MyMesh>::RemoveDegenerateFace(mesh);
  
  // 删除非流形边
  int nonmanif = vcg::tri::Clean<MyMesh>::RemoveNonManifoldFace(mesh);
  
  std::cout << "删除: " << dup << " 重复顶点, "
            << degen << " 退化面, "
            << nonmanif << " 非流形面" << std::endl;
}
```

### 曲率计算
```cpp
#include <vcg/complex/algorithms/update/curvature.h>

void compute_curvature(MyMesh& mesh) {
  // 更新拓扑和法向
  vcg::tri::UpdateTopology<MyMesh>::FaceFace(mesh);
  vcg::tri::UpdateNormal<MyMesh>::PerVertexNormalizedPerFace(mesh);
  
  // 计算曲率
  vcg::tri::UpdateCurvature<MyMesh>::MeanAndGaussian(mesh);
  
  // 访问曲率值
  for(auto& v : mesh.vert) {
    float mean_curv = v.Kh();
    float gauss_curv = v.Kg();
  }
}
```

### 连通域分析
```cpp
#include <vcg/complex/algorithms/clustering.h>

void analyze_connected_components(MyMesh& mesh) {
  vcg::tri::UpdateTopology<MyMesh>::FaceFace(mesh);
  
  std::vector<std::pair<int, typename MyMesh::FacePointer>> components;
  int num = vcg::tri::Clean<MyMesh>::ConnectedComponents(mesh, components);
  
  std::cout << "连通域数量: " << num << std::endl;
}
```

## 📚 项目中使用的 VCGlib 功能

| 功能 | VCGlib 模块 | 对应的项目模块 |
|------|-------------|----------------|
| 网格平滑 | Smooth | 气泡修复、凹陷修复 |
| 网格清理 | Clean | 飞边处理 |
| 曲率计算 | UpdateCurvature | 自动牙齿分割 |
| 网格 I/O | io_trimesh | 输出模块 |
| 连通域 | Clean | 飞边处理 |

## ⚠️ 注意事项

1. **Header-only**: VCGlib 是纯头文件库，包含即可使用
2. **编译时间**: 由于大量模板，编译时间较长
3. **许可证**: GPL v3，商业使用需注意
4. **C++11+**: 需要 C++11 或更高版本
5. **包含路径**: 正确设置包含路径很重要

## 🔗 相关资源

- [官方文档](http://vcg.isti.cnr.it/vcglib/index.html)
- [GitHub Wiki](https://github.com/cnr-isti-vclab/vcglib/wiki)
- [示例代码](https://github.com/cnr-isti-vclab/vcglib/tree/main/apps/sample)
- [MeshLab](http://www.meshlab.net/) - 基于 VCGlib 的开源工具

## 🐛 常见问题

### 1. 编译错误：找不到头文件
```cmake
# 确保包含路径正确
include_directories(${CMAKE_SOURCE_DIR}/third_party/vcglib)
```

### 2. 模板实例化错误
```cpp
// 确保包含必要的更新算法
#include <vcg/complex/algorithms/update/topology.h>
#include <vcg/complex/algorithms/update/normal.h>
#include <vcg/complex/algorithms/update/bounding.h>
```

### 3. 与 Eigen 冲突
```cpp
// 在包含 VCGlib 前定义
#define VCG_USE_EIGEN
#include <vcg/...>
```

---

**状态**: ✅ 已配置（源码需要克隆）
**最后检查**: 2025-11-03
**安装命令**: `cd /workspace/third_party && git clone https://github.com/cnr-isti-vclab/vcglib.git`
