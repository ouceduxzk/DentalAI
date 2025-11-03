# FindNlohmannJson.cmake - Find nlohmann/json
#
# Usage:
#   find_package(NlohmannJson REQUIRED)
#
# Sets:
#   NlohmannJson_FOUND - TRUE if nlohmann/json is found
#   NlohmannJson_INCLUDE_DIRS - Include directories

# 首先尝试使用 CMake 官方的 find_package
find_package(nlohmann_json QUIET)

if(nlohmann_json_FOUND)
  set(NlohmannJson_FOUND TRUE)
  set(NlohmannJson_INCLUDE_DIRS ${nlohmann_json_INCLUDE_DIRS})
  message(STATUS "Found nlohmann/json (system): ${nlohmann_json_VERSION}")
else()
  # 尝试查找本地头文件
  find_path(NlohmannJson_INCLUDE_DIR
    NAMES nlohmann/json.hpp json.hpp
    PATHS
      ${CMAKE_SOURCE_DIR}/third_party/json
      /usr/include
      /usr/local/include
    DOC "Path to nlohmann/json header"
  )
  
  include(FindPackageHandleStandardArgs)
  find_package_handle_standard_args(NlohmannJson
    DEFAULT_MSG
    NlohmannJson_INCLUDE_DIR
  )
  
  if(NlohmannJson_FOUND)
    set(NlohmannJson_INCLUDE_DIRS ${NlohmannJson_INCLUDE_DIR})
    message(STATUS "Found nlohmann/json (local): ${NlohmannJson_INCLUDE_DIR}")
  else()
    message(WARNING "nlohmann/json not found. Downloading...")
    message(WARNING "  wget -O ${CMAKE_SOURCE_DIR}/third_party/json/json.hpp \\")
    message(WARNING "    https://github.com/nlohmann/json/releases/download/v3.11.3/json.hpp")
  endif()
  
  mark_as_advanced(NlohmannJson_INCLUDE_DIR)
endif()
