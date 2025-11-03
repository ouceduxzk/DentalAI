add_library(preprocessing STATIC
  auto_adjust_plane.cc
  manual_adjust_plane.cc
  flying_edge_removal.cc
  bubble_repair.cc
  depression_repair.cc
)

target_link_libraries(preprocessing
  PUBLIC
    common
    Eigen3::Eigen
    ${PCL_LIBRARIES}
    ${CGAL_LIBRARIES}
)

if(OpenMP_FOUND)
  target_link_libraries(preprocessing PUBLIC OpenMP::OpenMP_CXX)
endif()

target_include_directories(preprocessing
  PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
)
