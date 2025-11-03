# VTK - 可视化工具包

VTK (Visualization Toolkit) 是一个开源的 3D 计算机图形、图像处理和可视化软件系统。

## 📋 基本信息

- **官网**: https://vtk.org/
- **版本**: 9.0+
- **许可证**: BSD
- **类型**: 编译库

## 🎯 在本项目中的应用

### 使用模块

1. **可视化**
   - 3D 网格渲染
   - 实时预览
   - 交互式查看器
   
2. **数据处理**
   - 网格滤波
   - 数据转换
   - 空间查询
   
3. **文件 I/O**
   - STL、OBJ、PLY 等格式
   - VTK 原生格式

### 主要功能

- **渲染引擎**
  - 高性能 3D 渲染
  - 光照和材质
  - 相机控制
  
- **数据结构**
  - vtkPolyData（多边形数据）
  - vtkUnstructuredGrid（非结构化网格）
  
- **滤波器**
  - 网格平滑
  - 网格细分
  - 表面提取

## 🚀 安装

### Ubuntu/Debian
```bash
sudo apt-get install libvtk9-dev libvtk9-qt-dev
```

### macOS
```bash
brew install vtk
```

### Windows (vcpkg)
```bash
vcpkg install vtk
```

### 从源码编译
```bash
# 下载源码
git clone https://gitlab.kitware.com/vtk/vtk.git
cd vtk
git checkout v9.2.0

# 编译
mkdir build && cd build
cmake -DCMAKE_BUILD_TYPE=Release \
      -DVTK_GROUP_ENABLE_Qt=YES \
      -DVTK_MODULE_ENABLE_VTK_GUISupportQt=YES \
      ..
make -j$(nproc)
sudo make install
```

## 🔧 CMake 集成

```cmake
# 查找 VTK
find_package(VTK REQUIRED)
include(${VTK_USE_FILE})

# 链接 VTK
target_link_libraries(your_target ${VTK_LIBRARIES})

# 或使用现代 CMake
target_link_libraries(your_target 
  VTK::CommonCore
  VTK::CommonDataModel
  VTK::IOGeometry
  VTK::RenderingCore
  VTK::RenderingOpenGL2
  VTK::InteractionStyle
)
```

## 💡 使用示例

### 加载和显示 STL
```cpp
#include <vtkSmartPointer.h>
#include <vtkSTLReader.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkRenderer.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>

void visualize_stl(const std::string& filename) {
  // 读取 STL
  auto reader = vtkSmartPointer<vtkSTLReader>::New();
  reader->SetFileName(filename.c_str());
  reader->Update();
  
  // 创建 Mapper
  auto mapper = vtkSmartPointer<vtkPolyDataMapper>::New();
  mapper->SetInputConnection(reader->GetOutputPort());
  
  // 创建 Actor
  auto actor = vtkSmartPointer<vtkActor>::New();
  actor->SetMapper(mapper);
  
  // 创建 Renderer
  auto renderer = vtkSmartPointer<vtkRenderer>::New();
  renderer->AddActor(actor);
  renderer->SetBackground(0.1, 0.2, 0.3);
  
  // 创建 RenderWindow
  auto renderWindow = vtkSmartPointer<vtkRenderWindow>::New();
  renderWindow->AddRenderer(renderer);
  renderWindow->SetSize(800, 600);
  
  // 创建 Interactor
  auto interactor = vtkSmartPointer<vtkRenderWindowInteractor>::New();
  interactor->SetRenderWindow(renderWindow);
  
  // 开始交互
  renderWindow->Render();
  interactor->Start();
}
```

### 网格平滑
```cpp
#include <vtkSmoothPolyDataFilter.h>

vtkSmartPointer<vtkPolyData> smooth_mesh(vtkPolyData* input, int iterations = 10) {
  auto smoother = vtkSmartPointer<vtkSmoothPolyDataFilter>::New();
  smoother->SetInputData(input);
  smoother->SetNumberOfIterations(iterations);
  smoother->SetRelaxationFactor(0.1);
  smoother->FeatureEdgeSmoothingOff();
  smoother->BoundarySmoothingOn();
  smoother->Update();
  
  return smoother->GetOutput();
}
```

### 保存网格
```cpp
#include <vtkSTLWriter.h>
#include <vtkPLYWriter.h>
#include <vtkOBJWriter.h>

void save_stl(vtkPolyData* mesh, const std::string& filename) {
  auto writer = vtkSmartPointer<vtkSTLWriter>::New();
  writer->SetFileName(filename.c_str());
  writer->SetInputData(mesh);
  writer->Write();
}

void save_ply(vtkPolyData* mesh, const std::string& filename) {
  auto writer = vtkSmartPointer<vtkPLYWriter>::New();
  writer->SetFileName(filename.c_str());
  writer->SetInputData(mesh);
  writer->Write();
}
```

### 网格清理
```cpp
#include <vtkCleanPolyData.h>

vtkSmartPointer<vtkPolyData> clean_mesh(vtkPolyData* input) {
  auto cleaner = vtkSmartPointer<vtkCleanPolyData>::New();
  cleaner->SetInputData(input);
  cleaner->Update();
  return cleaner->GetOutput();
}
```

### 计算法向
```cpp
#include <vtkPolyDataNormals.h>

vtkSmartPointer<vtkPolyData> compute_normals(vtkPolyData* input) {
  auto normals = vtkSmartPointer<vtkPolyDataNormals>::New();
  normals->SetInputData(input);
  normals->ComputePointNormalsOn();
  normals->ComputeCellNormalsOn();
  normals->ConsistencyOn();
  normals->AutoOrientNormalsOn();
  normals->Update();
  
  return normals->GetOutput();
}
```

## 📚 常用类

| 类名 | 功能 | 用途 |
|------|------|------|
| vtkSTLReader | STL 读取 | 加载模型 |
| vtkSTLWriter | STL 写入 | 保存模型 |
| vtkPolyData | 多边形数据 | 网格表示 |
| vtkPolyDataMapper | 数据映射 | 渲染准备 |
| vtkActor | 场景对象 | 渲染对象 |
| vtkRenderer | 渲染器 | 场景管理 |
| vtkSmoothPolyDataFilter | 平滑滤波 | 网格平滑 |
| vtkCleanPolyData | 清理网格 | 网格修复 |

## ⚙️ 性能优化

```cpp
// 使用智能指针避免内存泄漏
#include <vtkSmartPointer.h>

// 启用多线程
#include <vtkMultiThreader.h>
vtkMultiThreader::SetGlobalMaximumNumberOfThreads(8);

// 优化渲染
renderer->SetUseFXAA(true);  // 抗锯齿
renderWindow->SetMultiSamples(4);  // 多重采样
```

## 🔗 相关资源

- [官方文档](https://vtk.org/documentation/)
- [示例代码](https://kitware.github.io/vtk-examples/site/)
- [VTK 教程](https://vtk.org/Wiki/VTK/Tutorials)
- [VTK User's Guide](https://www.kitware.com/products/books/VTKUsersGuide.pdf)

## ⚠️ 注意事项

1. **库体积**: VTK 非常庞大，编译和安装需要较长时间
2. **内存管理**: 使用 vtkSmartPointer 管理对象生命周期
3. **线程安全**: 部分功能不是线程安全的
4. **Qt 集成**: 如需 Qt，需要编译时启用 VTK_GROUP_ENABLE_Qt

## 🐛 常见问题

### 1. 找不到 VTK
```bash
# 手动指定路径
cmake -DVTK_DIR=/usr/local/lib/cmake/vtk-9.2 ..
```

### 2. 链接错误
```cmake
# 使用现代 CMake 目标
find_package(VTK 9.0 REQUIRED)
target_link_libraries(your_target ${VTK_LIBRARIES})
```

### 3. 渲染窗口不显示
```cpp
// 确保调用 Render() 和 Start()
renderWindow->Render();
interactor->Start();
```

---

**状态**: ⚠️ 需要安装
**安装命令**: `sudo apt-get install libvtk9-dev`
**最后检查**: 2025-11-03
