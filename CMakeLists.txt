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
find_package(PCL 1.10 REQUIRED)
find_package(CGAL REQUIRED)
find_package(OpenMP)

# Optional packages
find_package(Qt5 COMPONENTS Core Widgets OpenGL)

# Include directories
include_directories(
  ${CMAKE_SOURCE_DIR}/include
  ${CMAKE_SOURCE_DIR}/src
  ${EIGEN3_INCLUDE_DIR}
  ${PCL_INCLUDE_DIRS}
  ${CGAL_INCLUDE_DIRS}
)

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
message(STATUS "Eigen3: ${EIGEN3_VERSION}")
message(STATUS "PCL: ${PCL_VERSION}")
message(STATUS "CGAL: ${CGAL_VERSION}")
if(OpenMP_FOUND)
  message(STATUS "OpenMP: Enabled")
else()
  message(STATUS "OpenMP: Disabled")
endif()
if(Qt5_FOUND)
  message(STATUS "Qt5: ${Qt5_VERSION}")
else()
  message(STATUS "Qt5: Not found (GUI features disabled)")
endif()
