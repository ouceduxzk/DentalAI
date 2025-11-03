# nlohmann/json - JSON 库

nlohmann/json 是一个现代 C++ JSON 库，易用且功能强大。

## 📋 基本信息

- **GitHub**: https://github.com/nlohmann/json
- **版本**: 3.11.0+
- **许可证**: MIT
- **类型**: Header-only（单头文件）

## 🎯 在本项目中的应用

### 使用场景

1. **配置文件**
   - 读取参数配置
   - 保存用户设置
   
2. **数据序列化**
   - 牙齿信息序列化
   - 特征点数据保存
   - AI 模型元数据
   
3. **数据交换**
   - 模块间数据传递
   - 导出分析结果

## 🚀 安装

### Ubuntu/Debian
```bash
sudo apt-get install nlohmann-json3-dev
```

### macOS
```bash
brew install nlohmann-json
```

### Windows (vcpkg)
```bash
vcpkg install nlohmann-json
```

### 手动安装（Header-only）
```bash
# 下载单头文件
cd /workspace/third_party/json
wget https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp
```

## 🔧 CMake 集成

### 方式 1: 系统安装
```cmake
find_package(nlohmann_json 3.7.0 REQUIRED)
target_link_libraries(your_target nlohmann_json::nlohmann_json)
```

### 方式 2: 单头文件
```cmake
include_directories(${CMAKE_SOURCE_DIR}/third_party/json)
# 无需链接，直接包含使用
```

## 💡 使用示例

### 基本用法
```cpp
#include <nlohmann/json.hpp>
#include <iostream>
#include <fstream>

// 使用别名简化
using json = nlohmann::json;

int main() {
  // 创建 JSON 对象
  json config;
  config["version"] = "1.0.0";
  config["max_iterations"] = 100;
  config["tolerance"] = 0.001;
  config["enable_gpu"] = true;
  
  // 数组
  config["modules"] = {"preprocessing", "segmentation", "reconstruction"};
  
  // 嵌套对象
  config["preprocessing"]["auto_adjust"] = true;
  config["preprocessing"]["smooth_iterations"] = 10;
  
  // 输出 JSON（美化）
  std::cout << config.dump(4) << std::endl;
  
  // 保存到文件
  std::ofstream file("config.json");
  file << config.dump(4);
  file.close();
  
  return 0;
}
```

### 读取配置文件
```cpp
#include <nlohmann/json.hpp>
#include <fstream>

struct Config {
  int max_iterations;
  double tolerance;
  bool enable_gpu;
  std::vector<std::string> modules;
};

Config load_config(const std::string& filename) {
  // 读取文件
  std::ifstream file(filename);
  json j;
  file >> j;
  
  // 解析配置
  Config config;
  config.max_iterations = j["max_iterations"];
  config.tolerance = j["tolerance"];
  config.enable_gpu = j["enable_gpu"];
  config.modules = j["modules"].get<std::vector<std::string>>();
  
  return config;
}
```

### 牙齿数据序列化
```cpp
#include <nlohmann/json.hpp>
#include <vector>

struct Point3D {
  double x, y, z;
};

struct Tooth {
  int id;
  std::string type;
  Point3D centroid;
  std::vector<Point3D> landmarks;
};

// Point3D 序列化
void to_json(json& j, const Point3D& p) {
  j = json{{"x", p.x}, {"y", p.y}, {"z", p.z}};
}

void from_json(const json& j, Point3D& p) {
  j.at("x").get_to(p.x);
  j.at("y").get_to(p.y);
  j.at("z").get_to(p.z);
}

// Tooth 序列化
void to_json(json& j, const Tooth& t) {
  j = json{
    {"id", t.id},
    {"type", t.type},
    {"centroid", t.centroid},
    {"landmarks", t.landmarks}
  };
}

void from_json(const json& j, Tooth& t) {
  j.at("id").get_to(t.id);
  j.at("type").get_to(t.type);
  j.at("centroid").get_to(t.centroid);
  j.at("landmarks").get_to(t.landmarks);
}

// 使用示例
void save_teeth(const std::vector<Tooth>& teeth, const std::string& filename) {
  json j = teeth;
  std::ofstream file(filename);
  file << j.dump(4);
}

std::vector<Tooth> load_teeth(const std::string& filename) {
  std::ifstream file(filename);
  json j;
  file >> j;
  return j.get<std::vector<Tooth>>();
}
```

### 分析结果导出
```cpp
json export_analysis_results(const std::vector<Tooth>& teeth) {
  json results;
  results["timestamp"] = "2025-11-03T10:30:00Z";
  results["total_teeth"] = teeth.size();
  
  json teeth_array = json::array();
  for (const auto& tooth : teeth) {
    json tooth_obj;
    tooth_obj["id"] = tooth.id;
    tooth_obj["type"] = tooth.type;
    tooth_obj["position"] = {
      {"x", tooth.centroid.x},
      {"y", tooth.centroid.y},
      {"z", tooth.centroid.z}
    };
    teeth_array.push_back(tooth_obj);
  }
  
  results["teeth"] = teeth_array;
  return results;
}
```

### 错误处理
```cpp
#include <nlohmann/json.hpp>

void safe_read_json(const std::string& filename) {
  try {
    std::ifstream file(filename);
    json j;
    file >> j;
    
    // 安全访问（如果键不存在，会抛出异常）
    int iterations = j.at("max_iterations");
    
    // 或提供默认值
    int max_iter = j.value("max_iterations", 100);
    
    // 检查键是否存在
    if (j.contains("tolerance")) {
      double tol = j["tolerance"];
    }
    
  } catch (const json::parse_error& e) {
    std::cerr << "JSON 解析错误: " << e.what() << std::endl;
  } catch (const json::type_error& e) {
    std::cerr << "JSON 类型错误: " << e.what() << std::endl;
  } catch (const json::out_of_range& e) {
    std::cerr << "JSON 键不存在: " << e.what() << std::endl;
  }
}
```

## 📚 项目中的应用场景

| 功能 | JSON 用途 | 文件示例 |
|------|-----------|---------|
| 配置管理 | 保存算法参数 | `config/preprocessing.json` |
| 牙齿数据 | 序列化牙齿信息 | `output/teeth_data.json` |
| 特征点 | 保存标志点坐标 | `output/landmarks.json` |
| 分析结果 | 导出分析报告 | `output/analysis_report.json` |
| AI 模型 | 模型元数据 | `models/segmentation_meta.json` |

## 配置文件示例

### preprocessing_config.json
```json
{
  "auto_adjust_plane": {
    "method": "pca",
    "tolerance": 0.01
  },
  "flying_edge_removal": {
    "max_iterations": 5,
    "min_component_size": 100
  },
  "bubble_repair": {
    "smooth_iterations": 10,
    "smooth_factor": 0.5
  }
}
```

### teeth_data.json
```json
{
  "patient_id": "P12345",
  "scan_date": "2025-11-03",
  "teeth": [
    {
      "id": 11,
      "type": "incisor",
      "centroid": {"x": 10.5, "y": 20.3, "z": 5.1},
      "landmarks": [
        {"x": 10.0, "y": 20.0, "z": 5.0},
        {"x": 11.0, "y": 20.5, "z": 5.2}
      ]
    }
  ]
}
```

## ⚠️ 注意事项

1. **Header-only**: 单头文件，编译时间可能较长
2. **异常处理**: 使用 try-catch 捕获 JSON 异常
3. **编码**: 默认使用 UTF-8
4. **性能**: 对于大数据，考虑使用二进制格式（如 MessagePack）

## 🔗 相关资源

- [官方文档](https://json.nlohmann.me/)
- [GitHub](https://github.com/nlohmann/json)
- [在线工具](https://json.nlohmann.me/api/basic_json/)
- [性能对比](https://github.com/nlohmann/json#performance)

## 🐛 常见问题

### 1. 找不到 json.hpp
```cmake
# 添加包含路径
include_directories(${CMAKE_SOURCE_DIR}/third_party/json)
```

### 2. 编译时间过长
```cpp
// 使用前向声明头文件（仅在必要时包含完整头文件）
#include <nlohmann/json_fwd.hpp>
```

### 3. 与其他 JSON 库冲突
```cpp
// 使用命名空间
namespace nlohmann {
  // ...
}
```

---

**状态**: ✅ 已包含（单头文件）
**文件位置**: `/workspace/third_party/json/json.hpp`
**最后检查**: 2025-11-03
