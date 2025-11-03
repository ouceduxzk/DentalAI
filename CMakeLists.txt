cmake_minimum_required(VERSION 3.16)
project(DentalSegmentation VERSION 1.0.0 LANGUAGES CXX)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set build type if not specified
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# Add custom CMake module path for third-party libraries
list(APPEND CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/third_party/cmake")

# Compiler flags following Google C++ Style Guide
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")

# Output directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# Find required packages
find_package(Eigen3 3.3 REQUIRED NO_MODULE)
find_package(CGAL REQUIRED)
find_package(OpenMP)

# Optional packages  
find_package(PCL 1.10 QUIET)
find_package(Qt5 COMPONENTS Core Widgets OpenGL QUIET)
find_package(VTK QUIET)

# Third-party libraries in third_party/
find_package(VCG QUIET)
find_package(NlohmannJson QUIET)

# Testing framework
find_package(GTest QUIET)

# Include directories
include_directories(
  ${CMAKE_SOURCE_DIR}/include
  ${CMAKE_SOURCE_DIR}/src
  ${EIGEN3_INCLUDE_DIR}
  ${CGAL_INCLUDE_DIRS}
)

# Add PCL if found
if(PCL_FOUND)
  include_directories(${PCL_INCLUDE_DIRS})
  add_definitions(${PCL_DEFINITIONS})
endif()

# Add VTK if found
if(VTK_FOUND)
  include(${VTK_USE_FILE})
endif()

# Add VCGlib if found
if(VCG_FOUND)
  include_directories(${VCG_INCLUDE_DIRS})
  add_definitions(-DUSE_VCGLIB)
endif()

# Add nlohmann/json
if(NlohmannJson_FOUND)
  include_directories(${NlohmannJson_INCLUDE_DIRS})
else()
  # Fallback to local copy
  include_directories(${CMAKE_SOURCE_DIR}/third_party/json)
endif()

# Add subdirectories
add_subdirectory(src/common)
add_subdirectory(src/preprocessing)
add_subdirectory(src/segmentation)
add_subdirectory(src/reconstruction)
add_subdirectory(src/analysis)
add_subdirectory(src/output)

# Testing
enable_testing()
add_subdirectory(tests)

# Installation
install(DIRECTORY include/ DESTINATION include)

# Print configuration summary
message(STATUS "=== Configuration Summary ===")
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ standard: ${CMAKE_CXX_STANDARD}")
message(STATUS "Compiler: ${CMAKE_CXX_COMPILER_ID} ${CMAKE_CXX_COMPILER_VERSION}")
message(STATUS "")
message(STATUS "=== Required Libraries ===")
message(STATUS "Eigen3: ${EIGEN3_VERSION}")
message(STATUS "CGAL: ${CGAL_VERSION}")
message(STATUS "")
message(STATUS "=== Optional Libraries ===")
if(OpenMP_FOUND)
  message(STATUS "OpenMP: Enabled")
else()
  message(STATUS "OpenMP: Disabled")
endif()
if(PCL_FOUND)
  message(STATUS "PCL: ${PCL_VERSION}")
else()
  message(STATUS "PCL: Not found (optional)")
endif()
if(Qt5_FOUND)
  message(STATUS "Qt5: ${Qt5_VERSION}")
else()
  message(STATUS "Qt5: Not found (GUI features disabled)")
endif()
if(VTK_FOUND)
  message(STATUS "VTK: ${VTK_VERSION}")
else()
  message(STATUS "VTK: Not found (visualization disabled)")
endif()
if(VCG_FOUND)
  message(STATUS "VCGlib: Found")
else()
  message(STATUS "VCGlib: Not found (clone to third_party/vcglib)")
endif()
if(NlohmannJson_FOUND)
  message(STATUS "nlohmann/json: Found")
else()
  message(STATUS "nlohmann/json: Using local copy")
endif()
if(GTest_FOUND)
  message(STATUS "Google Test: Found")
else()
  message(STATUS "Google Test: Not found (testing disabled)")
endif()
message(STATUS "")
message(STATUS "=== AI Models ===")
message(STATUS "Tooth Segmentation: models/tooth_segmentation.onnx (Ready)")
message(STATUS "Landmark Detection: models/landmark_detection.onnx (Ready)")
message(STATUS "")
