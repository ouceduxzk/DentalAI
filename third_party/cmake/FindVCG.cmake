# FindVCG.cmake - Find VCGlib
#
# Usage:
#   find_package(VCG REQUIRED)
#
# Sets:
#   VCG_FOUND - TRUE if VCGlib is found
#   VCG_INCLUDE_DIRS - Include directories for VCGlib

find_path(VCG_INCLUDE_DIR
  NAMES vcg/complex/complex.h
  PATHS
    ${CMAKE_SOURCE_DIR}/third_party/vcglib
    ${CMAKE_SOURCE_DIR}/third_party/vcglib/src
    /usr/include
    /usr/local/include
  DOC "Path to VCGlib headers"
)

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(VCG
  DEFAULT_MSG
  VCG_INCLUDE_DIR
)

if(VCG_FOUND)
  set(VCG_INCLUDE_DIRS ${VCG_INCLUDE_DIR})
  message(STATUS "Found VCGlib: ${VCG_INCLUDE_DIR}")
else()
  message(WARNING "VCGlib not found. Please clone it to third_party/vcglib")
  message(WARNING "  cd ${CMAKE_SOURCE_DIR}/third_party")
  message(WARNING "  git clone https://github.com/cnr-isti-vclab/vcglib.git")
endif()

mark_as_advanced(VCG_INCLUDE_DIR)
