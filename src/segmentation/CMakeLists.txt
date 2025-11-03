add_library(segmentation STATIC
  gingival_margin_drawing.cc
  tooth_contour_editing.cc
  tooth_numbering.cc
  proximal_surface_segmentation.cc
  landmark_marking.cc
  auto_tooth_segmentation.cc
  auto_tooth_numbering.cc
)

target_link_libraries(segmentation
  PUBLIC
    common
    Eigen3::Eigen
    ${PCL_LIBRARIES}
)

if(OpenMP_FOUND)
  target_link_libraries(segmentation PUBLIC OpenMP::OpenMP_CXX)
endif()

target_include_directories(segmentation
  PUBLIC
    ${CMAKE_SOURCE_DIR}/include
    ${CMAKE_SOURCE_DIR}/src
)
