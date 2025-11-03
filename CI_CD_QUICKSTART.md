# GitLab CI/CD 快速开始指南 🚀

本指南帮助你快速配置和使用 GitLab CI/CD 来自动构建和测试项目。

## ✅ 前提条件

- GitLab 仓库已经创建
- GitLab Runner 已配置（使用 Docker executor）
- 项目已推送到 GitLab

## 🎯 快速步骤

### 1. 推送 CI/CD 配置

项目已包含以下文件：
- `.gitlab-ci.yml` - CI/CD 配置文件
- `Dockerfile.ci` - CI 环境的 Docker 镜像定义
- `.gitlab-ci-docs.md` - 详细文档

确保这些文件已提交到仓库：

```bash
git add .gitlab-ci.yml Dockerfile.ci .gitlab-ci-docs.md CI_CD_QUICKSTART.md
git commit -m "添加 GitLab CI/CD 配置"
git push origin your-branch
```

### 2. 查看 Pipeline 运行

推送后，GitLab 会自动触发 Pipeline：

1. 访问你的 GitLab 项目
2. 点击左侧菜单 **CI/CD** → **Pipelines**
3. 查看最新的 Pipeline 运行状态

### 3. 查看测试结果

Pipeline 完成后：

1. 点击 Pipeline → **Tests** 标签查看测试结果
2. 绿色 ✅ 表示所有测试通过
3. 红色 ❌ 表示有测试失败，点击查看详情

## 🔧 优化建议

### 方案 A: 使用预构建 Docker 镜像（推荐⭐）

构建包含所有依赖的 Docker 镜像可以大幅加速 CI/CD：

```bash
# 1. 构建镜像
docker build -f Dockerfile.ci -t dental-ci:latest .

# 2. 推送到 GitLab Container Registry
docker login registry.gitlab.com
docker tag dental-ci:latest registry.gitlab.com/YOUR_GROUP/YOUR_PROJECT/ci:latest
docker push registry.gitlab.com/YOUR_GROUP/YOUR_PROJECT/ci:latest

# 3. 更新 .gitlab-ci.yml
# 将 image 改为: registry.gitlab.com/YOUR_GROUP/YOUR_PROJECT/ci:latest
# 删除或注释掉 before_script 中的依赖安装部分
```

### 方案 B: 使用 GitLab 的共享 Runner（默认）

当前配置会在每次运行时安装依赖。优点是简单，缺点是较慢（约 5-10 分钟）。

## 📊 Pipeline 阶段说明

### Build (构建)
- ✅ `build:release` - 构建 Release 版本（每次运行）
- 🔍 `build:debug` - 构建 Debug 版本（MR 和主分支）

### Test (测试)
- ✅ `test:unit` - 运行单元测试（每次运行）
- 🔍 `test:debug` - Debug 模式测试
- 📋 `code:quality` - 代码质量检查（cppcheck）
- 💾 `test:memory` - 内存泄漏检查（valgrind）

### Deploy (部署)
- 📚 `pages` - 生成文档（仅 main 分支）

## 🎮 常用操作

### 在本地复现 CI 环境

```bash
# 方式 1: 使用 Docker
docker run -it --rm -v $(pwd):/workspace ubuntu:22.04
# 然后在容器中按照 .gitlab-ci.yml 的步骤执行

# 方式 2: 使用本地构建脚本
./build.sh  # 这会构建并运行测试
```

### 跳过 CI

如果只是更新文档，不需要运行 CI：

```bash
git commit -m "更新文档 [ci skip]"
```

### 只运行特定 Job

在 GitLab UI 中：
1. 进入 Pipelines
2. 点击右上角 "Run Pipeline"
3. 选择要运行的 Job

### 查看失败原因

```bash
# 查看构建日志
# 在 GitLab UI: Pipeline → 点击失败的 Job → 查看日志

# 本地调试
./build.sh --debug  # 使用 Debug 模式构建
cd build
ctest --output-on-failure --verbose  # 详细测试输出
```

## 🐛 常见问题

### 问题 1: Pipeline 找不到依赖

**现象**: 报错 `Could not find Eigen3` 等

**解决**:
- 检查 `.gitlab-ci.yml` 中的 `before_script` 是否正确
- 或使用预构建的 Docker 镜像

### 问题 2: 测试失败

**现象**: `test:unit` job 失败

**解决**:
1. 在本地运行测试：`./build.sh && cd build && ctest --verbose`
2. 修复失败的测试
3. 重新提交

### 问题 3: Pipeline 太慢

**解决**: 使用预构建的 Docker 镜像（见上方"方案 A"）

### 问题 4: GitLab Runner 未配置

**现象**: Pipeline 一直显示 "pending"

**解决**: 
- 联系管理员配置 GitLab Runner
- 或在项目 Settings → CI/CD → Runners 中配置

## 📖 进阶使用

### 1. 添加代码覆盖率

在 `tests/CMakeLists.txt` 中添加：

```cmake
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  target_compile_options(dental_tests PRIVATE --coverage)
  target_link_libraries(dental_tests PRIVATE --coverage)
endif()
```

### 2. 生成测试报告

安装 `gtest-xml-output`：

```bash
cd build
GTEST_OUTPUT="xml:test_results.xml" ./bin/dental_tests
```

### 3. 配置通知

在 GitLab 项目中：
- Settings → Integrations → 配置 Slack/Email 等通知

## 🎓 下一步

1. 阅读详细文档：[.gitlab-ci-docs.md](.gitlab-ci-docs.md)
2. 自定义 Pipeline：修改 `.gitlab-ci.yml`
3. 添加更多测试：在 `tests/` 目录添加测试文件
4. 配置自动部署：添加部署脚本

## 📞 获取帮助

- 查看详细文档：`.gitlab-ci-docs.md`
- 查看 GitLab CI/CD 官方文档：https://docs.gitlab.com/ee/ci/
- 项目问题：提交 Issue

---

**快速链接**:
- [GitLab Pipeline](https://gitlab.com/YOUR_GROUP/YOUR_PROJECT/-/pipelines) 
- [Test Results](https://gitlab.com/YOUR_GROUP/YOUR_PROJECT/-/pipelines?scope=finished)
- [CI/CD Settings](https://gitlab.com/YOUR_GROUP/YOUR_PROJECT/-/settings/ci_cd)

**提示**: 将上方的 `YOUR_GROUP` 和 `YOUR_PROJECT` 替换为你的实际路径。

---

**版本**: v1.0  
**日期**: 2025-11-03
