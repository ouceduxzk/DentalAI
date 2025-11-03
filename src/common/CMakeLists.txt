add_library(common STATIC
  types.cc
  mesh_utils.cc
  geometry_utils.cc
)

target_link_libraries(common
  PUBLIC
    Eigen3::Eigen
    ${PCL_LIBRARIES}
    ${CGAL_LIBRARIES}
)

target_include_directories(common
  PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
)
