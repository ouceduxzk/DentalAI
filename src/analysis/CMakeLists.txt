add_library(analysis STATIC
  landmark_detection.cc
  ipr_simulation.cc
  gingiva_animation.cc
  arch_curve_analysis.cc
  spee_curve_analysis.cc
  angle_classification.cc
  overjet_overbite_analysis.cc
)

target_link_libraries(analysis
  PUBLIC
    common
    Eigen3::Eigen
)

target_include_directories(analysis
  PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
)
