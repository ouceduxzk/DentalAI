add_library(reconstruction STATIC
  auto_tooth_axis.cc
  manual_tooth_axis.cc
  auto_proximal_reconstruction.cc
  manual_proximal_reconstruction.cc
  crown_repair.cc
  virtual_gingiva_reconstruction.cc
  root_simulation.cc
)

target_link_libraries(reconstruction
  PUBLIC
    common
    Eigen3::Eigen
    ${CGAL_LIBRARIES}
)

target_include_directories(reconstruction
  PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
)
