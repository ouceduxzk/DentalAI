#!/bin/bash
# Quick build script for Dental Segmentation Project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== Dental Segmentation Build Script ===${NC}"

# Parse arguments
BUILD_TYPE="Release"
BUILD_TESTS="ON"
CLEAN_BUILD=false
NUM_JOBS=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4)

while [[ $# -gt 0 ]]; do
  case $1 in
    --debug)
      BUILD_TYPE="Debug"
      shift
      ;;
    --no-tests)
      BUILD_TESTS="OFF"
      shift
      ;;
    --clean)
      CLEAN_BUILD=true
      shift
      ;;
    -j*)
      NUM_JOBS="${1#-j}"
      shift
      ;;
    --help)
      echo "Usage: $0 [OPTIONS]"
      echo "Options:"
      echo "  --debug       Build in Debug mode (default: Release)"
      echo "  --no-tests    Don't build tests"
      echo "  --clean       Clean build directory before building"
      echo "  -jN           Use N parallel jobs (default: auto-detect)"
      echo "  --help        Show this help message"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      exit 1
      ;;
  esac
done

# Clean if requested
if [ "$CLEAN_BUILD" = true ]; then
  echo -e "${YELLOW}Cleaning build directory...${NC}"
  rm -rf build
fi

# Create build directory
mkdir -p build
cd build

# Configure
echo -e "${GREEN}Configuring CMake (Build Type: $BUILD_TYPE)...${NC}"
cmake .. \
  -DCMAKE_BUILD_TYPE=$BUILD_TYPE \
  -DBUILD_TESTING=$BUILD_TESTS \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

# Build
echo -e "${GREEN}Building with $NUM_JOBS parallel jobs...${NC}"
make -j$NUM_JOBS

# Run tests if enabled
if [ "$BUILD_TESTS" = "ON" ]; then
  echo -e "${GREEN}Running tests...${NC}"
  ctest --output-on-failure
fi

echo -e "${GREEN}=== Build completed successfully! ===${NC}"
echo -e "Binaries are in: ${YELLOW}build/bin/${NC}"
echo -e "Libraries are in: ${YELLOW}build/lib/${NC}"
