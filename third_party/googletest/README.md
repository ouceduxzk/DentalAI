# Google Test - C++ 测试框架

Google Test（GTest）是 Google 开发的 C++ 测试框架，用于编写和运行单元测试。

## 📋 基本信息

- **GitHub**: https://github.com/google/googletest
- **版本**: 1.14.0+
- **许可证**: BSD-3-Clause
- **类型**: 编译库

## 🎯 在本项目中的应用

### 测试范围

1. **单元测试**
   - 公共工具函数测试
   - 几何算法测试
   - 网格处理测试
   
2. **模块测试**
   - 预处理模块
   - 分割模块
   - 重建模块
   - 分析模块
   
3. **集成测试**
   - 完整工作流测试
   - 模块间交互测试

## 🚀 安装

### Ubuntu/Debian
```bash
sudo apt-get install libgtest-dev

# 编译静态库
cd /usr/src/gtest
sudo cmake .
sudo make
sudo cp lib/*.a /usr/lib
```

### macOS
```bash
brew install googletest
```

### Windows (vcpkg)
```bash
vcpkg install gtest
```

### CMake FetchContent（推荐）
```cmake
include(FetchContent)
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
  GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)
```

## 🔧 CMake 集成

```cmake
# 启用测试
enable_testing()

# 查找 GTest
find_package(GTest REQUIRED)
include(GoogleTest)

# 创建测试可执行文件
add_executable(test_geometry
  test_geometry_utils.cc
)

# 链接 GTest
target_link_libraries(test_geometry
  GTest::gtest
  GTest::gtest_main
  your_library
)

# 添加测试
gtest_discover_tests(test_geometry)

# 或手动添加
add_test(NAME test_geometry COMMAND test_geometry)
```

## 💡 使用示例

### 基本测试
```cpp
#include <gtest/gtest.h>
#include "geometry_utils.h"

// 简单测试
TEST(GeometryTest, DistanceCalculation) {
  Point3D p1{0, 0, 0};
  Point3D p2{3, 4, 0};
  
  double distance = CalculateDistance(p1, p2);
  
  EXPECT_DOUBLE_EQ(distance, 5.0);
}

// 带 Fixture 的测试
class MeshTest : public ::testing::Test {
 protected:
  void SetUp() override {
    // 初始化测试数据
    mesh_ = std::make_shared<Mesh>();
    LoadTestMesh(mesh_, "test_data/cube.stl");
  }
  
  void TearDown() override {
    // 清理
    mesh_.reset();
  }
  
  std::shared_ptr<Mesh> mesh_;
};

TEST_F(MeshTest, VertexCount) {
  ASSERT_NE(mesh_, nullptr);
  EXPECT_EQ(mesh_->vertices.size(), 8);  // 立方体有 8 个顶点
}

TEST_F(MeshTest, FaceCount) {
  ASSERT_NE(mesh_, nullptr);
  EXPECT_EQ(mesh_->faces.size(), 12);  // 立方体有 12 个面
}
```

### 几何工具测试
```cpp
#include <gtest/gtest.h>
#include "common/geometry_utils.h"

using namespace dental::geometry_utils;

TEST(GeometryUtilsTest, BSplineFitting) {
  std::vector<Point3D> points = {
    {0, 0, 0}, {1, 1, 0}, {2, 0.5, 0}, {3, 1.5, 0}
  };
  
  auto curve = FitBSpline(points, 3);
  
  ASSERT_FALSE(curve.empty());
  EXPECT_GE(curve.size(), points.size());
}

TEST(GeometryUtilsTest, PCAComputation) {
  std::vector<Point3D> points = {
    {1, 2, 3}, {2, 3, 4}, {3, 4, 5}
  };
  
  Eigen::Matrix3d axes;
  Eigen::Vector3d center;
  
  bool result = ComputePCA(points, &axes, &center);
  
  EXPECT_TRUE(result);
  EXPECT_NEAR(center.x(), 2.0, 1e-6);
  EXPECT_NEAR(center.y(), 3.0, 1e-6);
  EXPECT_NEAR(center.z(), 4.0, 1e-6);
}
```

### 网格工具测试
```cpp
#include <gtest/gtest.h>
#include "common/mesh_utils.h"

using namespace dental::mesh_utils;

class MeshUtilsTest : public ::testing::Test {
 protected:
  void SetUp() override {
    mesh_ = std::make_shared<Mesh>();
  }
  
  std::shared_ptr<Mesh> mesh_;
};

TEST_F(MeshUtilsTest, LoadSTL) {
  Status status = LoadMesh("test_data/tooth.stl", mesh_.get());
  
  EXPECT_TRUE(status.ok());
  EXPECT_GT(mesh_->vertices.size(), 0);
  EXPECT_GT(mesh_->faces.size(), 0);
}

TEST_F(MeshUtilsTest, ComputeNormals) {
  LoadMesh("test_data/tooth.stl", mesh_.get());
  
  Status status = ComputeNormals(mesh_.get());
  
  EXPECT_TRUE(status.ok());
  EXPECT_EQ(mesh_->normals.size(), mesh_->vertices.size());
  
  // 检查法向是否归一化
  for (const auto& normal : mesh_->normals) {
    double length = std::sqrt(normal.x * normal.x + 
                             normal.y * normal.y + 
                             normal.z * normal.z);
    EXPECT_NEAR(length, 1.0, 1e-6);
  }
}

TEST_F(MeshUtilsTest, LaplacianSmooth) {
  LoadMesh("test_data/noisy_mesh.stl", mesh_.get());
  
  auto original_vertices = mesh_->vertices;
  
  LaplacianSmoothConfig config;
  config.iterations = 10;
  config.lambda = 0.5;
  
  Status status = LaplacianSmooth(mesh_.get(), config);
  
  EXPECT_TRUE(status.ok());
  EXPECT_EQ(mesh_->vertices.size(), original_vertices.size());
  
  // 顶点位置应该有变化
  bool has_changed = false;
  for (size_t i = 0; i < mesh_->vertices.size(); ++i) {
    if (mesh_->vertices[i].x != original_vertices[i].x) {
      has_changed = true;
      break;
    }
  }
  EXPECT_TRUE(has_changed);
}
```

### 预处理模块测试
```cpp
#include <gtest/gtest.h>
#include "preprocessing/auto_adjust_plane.h"

using namespace dental::preprocessing;

TEST(AutoAdjustPlaneTest, ProcessValidMesh) {
  auto mesh = std::make_shared<Mesh>();
  LoadTestMesh(mesh, "test_data/dental_arch.stl");
  
  AutoAdjustPlane adjuster;
  CoordinateSystem cs;
  
  Status status = adjuster.Process(mesh, &cs);
  
  EXPECT_TRUE(status.ok());
  
  // 检查坐标系是否正交
  double dot_xy = cs.x_axis.dot(cs.y_axis);
  double dot_xz = cs.x_axis.dot(cs.z_axis);
  double dot_yz = cs.y_axis.dot(cs.z_axis);
  
  EXPECT_NEAR(dot_xy, 0.0, 1e-6);
  EXPECT_NEAR(dot_xz, 0.0, 1e-6);
  EXPECT_NEAR(dot_yz, 0.0, 1e-6);
}
```

### 参数化测试
```cpp
#include <gtest/gtest.h>

class SmoothTest : public ::testing::TestWithParam<int> {
  // 参数化测试
};

TEST_P(SmoothTest, DifferentIterations) {
  int iterations = GetParam();
  
  auto mesh = CreateTestMesh();
  LaplacianSmooth(mesh.get(), iterations);
  
  // 验证平滑效果
  EXPECT_TRUE(IsSmoother(mesh.get()));
}

INSTANTIATE_TEST_SUITE_P(
  IterationTests,
  SmoothTest,
  ::testing::Values(1, 5, 10, 20, 50)
);
```

### 死亡测试
```cpp
TEST(MeshUtilsDeathTest, NullPointer) {
  EXPECT_DEATH(LoadMesh("file.stl", nullptr), "");
}
```

## 📚 常用断言

### 布尔断言
- `EXPECT_TRUE(condition)`
- `EXPECT_FALSE(condition)`
- `ASSERT_TRUE(condition)` - 失败时终止测试

### 比较断言
- `EXPECT_EQ(a, b)` - 相等
- `EXPECT_NE(a, b)` - 不等
- `EXPECT_LT(a, b)` - 小于
- `EXPECT_GT(a, b)` - 大于

### 浮点数断言
- `EXPECT_FLOAT_EQ(a, b)`
- `EXPECT_DOUBLE_EQ(a, b)`
- `EXPECT_NEAR(a, b, tolerance)`

### 字符串断言
- `EXPECT_STREQ(str1, str2)`
- `EXPECT_STRCASEEQ(str1, str2)` - 忽略大小写

## 🏃 运行测试

```bash
# 编译测试
mkdir build && cd build
cmake ..
make

# 运行所有测试
ctest

# 或直接运行
./test_geometry_utils
./test_mesh_utils

# 运行特定测试
./test_geometry_utils --gtest_filter=GeometryTest.*

# 详细输出
./test_geometry_utils --gtest_verbose

# 生成 XML 报告
./test_geometry_utils --gtest_output=xml:report.xml
```

## 📊 测试覆盖率

```bash
# 使用 gcov/lcov
cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_FLAGS="--coverage" ..
make
ctest
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_html
```

## ⚠️ 注意事项

1. **EXPECT vs ASSERT**: EXPECT 失败后继续，ASSERT 失败后终止
2. **Fixture**: 复杂测试使用 Fixture 共享设置代码
3. **测试独立性**: 每个测试应该独立，不依赖其他测试
4. **测试命名**: 使用描述性名称，清楚表达测试意图

## 🔗 相关资源

- [官方文档](https://google.github.io/googletest/)
- [入门指南](https://google.github.io/googletest/primer.html)
- [高级指南](https://google.github.io/googletest/advanced.html)
- [FAQ](https://google.github.io/googletest/faq.html)

---

**状态**: ✅ 已集成
**测试文件位置**: `/workspace/tests/`
**最后检查**: 2025-11-03
