find_package(GTest QUIET)

if(GTest_FOUND)
  enable_testing()
  
  # Test executable
  add_executable(dental_tests
    test_main.cc
    test_mesh_utils.cc
    test_geometry_utils.cc
    test_preprocessing.cc
    test_segmentation.cc
  )
  
  target_link_libraries(dental_tests
    PRIVATE
      common
      preprocessing
      segmentation
      reconstruction
      analysis
      output
      GTest::GTest
      GTest::Main
  )
  
  # Add tests
  add_test(NAME DentalTests COMMAND dental_tests)
  
  message(STATUS "Tests enabled")
else()
  message(STATUS "GTest not found, tests disabled")
endif()
