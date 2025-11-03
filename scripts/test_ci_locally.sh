#!/bin/bash
# 本地测试 CI/CD 流程的脚本
# 用于在推送到 GitLab 之前本地验证构建和测试

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  本地 CI/CD 测试脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 解析参数
SKIP_BUILD=false
SKIP_TEST=false
USE_DOCKER=false
CLEAN=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --skip-build)
      SKIP_BUILD=true
      shift
      ;;
    --skip-test)
      SKIP_TEST=true
      shift
      ;;
    --docker)
      USE_DOCKER=true
      shift
      ;;
    --clean)
      CLEAN=true
      shift
      ;;
    --help)
      echo "用法: $0 [选项]"
      echo ""
      echo "选项:"
      echo "  --skip-build   跳过构建阶段"
      echo "  --skip-test    跳过测试阶段"
      echo "  --docker       在 Docker 容器中运行（模拟 CI 环境）"
      echo "  --clean        清理构建目录后重新开始"
      echo "  --help         显示此帮助信息"
      echo ""
      echo "示例:"
      echo "  $0                      # 完整运行构建和测试"
      echo "  $0 --docker             # 在 Docker 中运行（最接近 CI）"
      echo "  $0 --skip-build         # 只运行测试"
      echo "  $0 --clean              # 清理后重新构建"
      exit 0
      ;;
    *)
      echo -e "${RED}未知选项: $1${NC}"
      echo "使用 --help 查看帮助"
      exit 1
      ;;
  esac
done

# 如果使用 Docker
if [ "$USE_DOCKER" = true ]; then
  echo -e "${YELLOW}在 Docker 容器中运行...${NC}"
  
  # 检查 Docker 是否可用
  if ! command -v docker &> /dev/null; then
    echo -e "${RED}错误: Docker 未安装或不可用${NC}"
    exit 1
  fi
  
  # 检查镜像是否存在
  if ! docker image inspect dental-ci:latest &> /dev/null; then
    echo -e "${YELLOW}Docker 镜像不存在，正在构建...${NC}"
    docker build -f Dockerfile.ci -t dental-ci:latest .
  fi
  
  # 在容器中运行此脚本（不使用 Docker 标志以避免递归）
  docker run -it --rm \
    -v "$(pwd):/workspace" \
    -w /workspace \
    dental-ci:latest \
    /workspace/scripts/test_ci_locally.sh \
    $([ "$SKIP_BUILD" = true ] && echo "--skip-build") \
    $([ "$SKIP_TEST" = true ] && echo "--skip-test") \
    $([ "$CLEAN" = true ] && echo "--clean")
  
  exit $?
fi

# 检查必要的工具
echo -e "${BLUE}[1/4] 检查依赖...${NC}"
MISSING_DEPS=()

if ! command -v cmake &> /dev/null; then
  MISSING_DEPS+=("cmake")
fi

if ! command -v g++ &> /dev/null && ! command -v clang++ &> /dev/null; then
  MISSING_DEPS+=("g++ 或 clang++")
fi

if [ ${#MISSING_DEPS[@]} -ne 0 ]; then
  echo -e "${RED}错误: 缺少以下依赖:${NC}"
  for dep in "${MISSING_DEPS[@]}"; do
    echo -e "  - ${dep}"
  done
  echo ""
  echo -e "${YELLOW}建议: 使用 --docker 选项在容器中运行${NC}"
  exit 1
fi

echo -e "${GREEN}✓ 依赖检查通过${NC}"
echo ""

# 清理
if [ "$CLEAN" = true ]; then
  echo -e "${BLUE}[清理] 删除构建目录...${NC}"
  rm -rf build build_debug
  echo -e "${GREEN}✓ 清理完成${NC}"
  echo ""
fi

# 构建阶段
if [ "$SKIP_BUILD" = false ]; then
  echo -e "${BLUE}[2/4] 构建阶段${NC}"
  echo -e "${YELLOW}--- 构建 Release 版本 ---${NC}"
  
  mkdir -p build
  cd build
  
  cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_TESTING=ON \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
  
  NUM_JOBS=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)
  make -j${NUM_JOBS}
  
  cd ..
  echo -e "${GREEN}✓ Release 构建完成${NC}"
  echo ""
  
  # 可选: 构建 Debug 版本
  if [ "${BUILD_DEBUG:-false}" = true ]; then
    echo -e "${YELLOW}--- 构建 Debug 版本 ---${NC}"
    mkdir -p build_debug
    cd build_debug
    
    cmake .. \
      -DCMAKE_BUILD_TYPE=Debug \
      -DBUILD_TESTING=ON \
      -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    
    make -j${NUM_JOBS}
    
    cd ..
    echo -e "${GREEN}✓ Debug 构建完成${NC}"
    echo ""
  fi
else
  echo -e "${YELLOW}[2/4] 跳过构建阶段${NC}"
  echo ""
fi

# 测试阶段
if [ "$SKIP_TEST" = false ]; then
  echo -e "${BLUE}[3/4] 测试阶段${NC}"
  
  if [ ! -d "build" ]; then
    echo -e "${RED}错误: 构建目录不存在，请先运行构建${NC}"
    exit 1
  fi
  
  echo -e "${YELLOW}--- 运行单元测试 ---${NC}"
  cd build
  
  if ctest --output-on-failure --verbose; then
    echo -e "${GREEN}✓ 所有测试通过${NC}"
    TEST_RESULT=0
  else
    echo -e "${RED}✗ 测试失败${NC}"
    TEST_RESULT=1
  fi
  
  cd ..
  echo ""
  
  # 代码质量检查（如果 cppcheck 可用）
  if command -v cppcheck &> /dev/null; then
    echo -e "${YELLOW}--- 代码质量检查 ---${NC}"
    cppcheck --enable=warning,style,performance,portability \
      --quiet \
      --inline-suppr \
      src/ 2>&1 | tee cppcheck-output.txt || true
    
    if [ -s cppcheck-output.txt ]; then
      echo -e "${YELLOW}⚠ 发现一些代码质量问题（见 cppcheck-output.txt）${NC}"
    else
      echo -e "${GREEN}✓ 代码质量检查通过${NC}"
    fi
    echo ""
  fi
else
  echo -e "${YELLOW}[3/4] 跳过测试阶段${NC}"
  TEST_RESULT=0
  echo ""
fi

# 总结
echo -e "${BLUE}[4/4] 总结${NC}"
echo -e "${BLUE}========================================${NC}"

if [ "$SKIP_BUILD" = false ]; then
  echo -e "${GREEN}✓ 构建: 成功${NC}"
else
  echo -e "${YELLOW}○ 构建: 已跳过${NC}"
fi

if [ "$SKIP_TEST" = false ]; then
  if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ 测试: 通过${NC}"
  else
    echo -e "${RED}✗ 测试: 失败${NC}"
  fi
else
  echo -e "${YELLOW}○ 测试: 已跳过${NC}"
fi

echo -e "${BLUE}========================================${NC}"
echo ""

if [ $TEST_RESULT -eq 0 ]; then
  echo -e "${GREEN}🎉 所有检查通过！代码可以推送到 GitLab${NC}"
  echo ""
  echo -e "${BLUE}下一步:${NC}"
  echo -e "  git add ."
  echo -e "  git commit -m \"你的提交信息\""
  echo -e "  git push origin your-branch"
  exit 0
else
  echo -e "${RED}❌ 存在失败的测试，请修复后再推送${NC}"
  echo ""
  echo -e "${BLUE}调试建议:${NC}"
  echo -e "  cd build"
  echo -e "  ctest --verbose --rerun-failed  # 重新运行失败的测试"
  exit 1
fi
