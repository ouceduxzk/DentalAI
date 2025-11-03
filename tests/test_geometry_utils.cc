// Copyright 2025 Dental Segmentation Project
// Geometry utilities tests

#include <gtest/gtest.h>
#include "common/geometry_utils.h"

namespace dental {
namespace geometry_utils {
namespace {

TEST(GeometryUtilsTest, PCAComputation) {
  // TODO: Implement test
  EXPECT_TRUE(true);
}

TEST(GeometryUtilsTest, PointToPointDistance) {
  Point3D p1(0, 0, 0);
  Point3D p2(1, 0, 0);
  double dist = PointToPointDistance(p1, p2);
  EXPECT_NEAR(dist, 1.0, 1e-6);
}

}  // namespace
}  // namespace geometry_utils
}  // namespace dental
