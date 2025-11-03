add_library(output STATIC
  mesh_exporter.cc
  mesh_with_gingiva_exporter.cc
)

target_link_libraries(output
  PUBLIC
    common
    ${CGAL_LIBRARIES}
)

target_include_directories(output
  PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
)
