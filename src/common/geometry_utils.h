// Copyright 2025 Dental Segmentation Project
// Geometry utility functions

#ifndef SRC_COMMON_GEOMETRY_UTILS_H_
#define SRC_COMMON_GEOMETRY_UTILS_H_

#include <vector>

#include "common/types.h"

namespace dental {
namespace geometry_utils {

// Distance calculations
double PointToPointDistance(const Point3D& p1, const Point3D& p2);
double PointToPlaneDistance(const Point3D& point, const Point3D& plane_point,
                            const Point3D& plane_normal);

// Curve fitting
std::vector<Point3D> FitBSpline(const std::vector<Point3D>& control_points,
                                 int num_samples);

// Shortest path on mesh surface
std::vector<int> DijkstraShortestPath(const MeshPtr& mesh, 
                                       int start_vertex,
                                       int end_vertex);

// PCA analysis
struct PCAResult {
  Point3D centroid;
  Eigen::Vector3d principal_axis1;
  Eigen::Vector3d principal_axis2;
  Eigen::Vector3d principal_axis3;
  Eigen::Vector3d eigenvalues;
};

PCAResult ComputePCA(const std::vector<Point3D>& points);

// Curvature calculation
double ComputeGaussianCurvature(const MeshPtr& mesh, int vertex_index);
double ComputeMeanCurvature(const MeshPtr& mesh, int vertex_index);

// Angle calculations
double ComputeAngleBetweenVectors(const Eigen::Vector3d& v1, 
                                   const Eigen::Vector3d& v2);

// Projection
Point3D ProjectPointOntoPlane(const Point3D& point, const Point3D& plane_point,
                               const Point3D& plane_normal);

// Intersection
bool RayTriangleIntersection(const Point3D& ray_origin,
                             const Eigen::Vector3d& ray_direction,
                             const Point3D& v0, const Point3D& v1,
                             const Point3D& v2, Point3D* intersection_point);

}  // namespace geometry_utils
}  // namespace dental

#endif  // SRC_COMMON_GEOMETRY_UTILS_H_
