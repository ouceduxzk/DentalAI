// Copyright 2025 Dental Segmentation Project
// Geometry utility functions implementation

#include "common/geometry_utils.h"

#include <cmath>
#include <queue>
#include <unordered_map>

namespace dental {
namespace geometry_utils {

double PointToPointDistance(const Point3D& p1, const Point3D& p2) {
  return (p1 - p2).norm();
}

double PointToPlaneDistance(const Point3D& point, const Point3D& plane_point,
                            const Point3D& plane_normal) {
  return std::abs((point - plane_point).dot(plane_normal));
}

std::vector<Point3D> FitBSpline(const std::vector<Point3D>& control_points,
                                 int num_samples) {
  // TODO: Implement B-spline curve fitting
  std::vector<Point3D> samples;
  return samples;
}

std::vector<int> DijkstraShortestPath(const MeshPtr& mesh, 
                                       int start_vertex,
                                       int end_vertex) {
  // TODO: Implement Dijkstra's algorithm on mesh surface
  std::vector<int> path;
  return path;
}

PCAResult ComputePCA(const std::vector<Point3D>& points) {
  PCAResult result;
  
  // Compute centroid
  result.centroid = Point3D::Zero();
  for (const auto& p : points) {
    result.centroid += p;
  }
  result.centroid /= static_cast<double>(points.size());
  
  // Compute covariance matrix
  Eigen::Matrix3d covariance = Eigen::Matrix3d::Zero();
  for (const auto& p : points) {
    Point3D centered = p - result.centroid;
    covariance += centered * centered.transpose();
  }
  covariance /= static_cast<double>(points.size());
  
  // Eigenvalue decomposition
  Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> solver(covariance);
  result.eigenvalues = solver.eigenvalues();
  
  // Sort by eigenvalues (descending order)
  result.principal_axis1 = solver.eigenvectors().col(2);
  result.principal_axis2 = solver.eigenvectors().col(1);
  result.principal_axis3 = solver.eigenvectors().col(0);
  
  return result;
}

double ComputeGaussianCurvature(const MeshPtr& mesh, int vertex_index) {
  // TODO: Implement Gaussian curvature computation
  return 0.0;
}

double ComputeMeanCurvature(const MeshPtr& mesh, int vertex_index) {
  // TODO: Implement mean curvature computation
  return 0.0;
}

double ComputeAngleBetweenVectors(const Eigen::Vector3d& v1, 
                                   const Eigen::Vector3d& v2) {
  double cos_angle = v1.dot(v2) / (v1.norm() * v2.norm());
  // Clamp to [-1, 1] to avoid numerical errors
  cos_angle = std::max(-1.0, std::min(1.0, cos_angle));
  return std::acos(cos_angle);
}

Point3D ProjectPointOntoPlane(const Point3D& point, const Point3D& plane_point,
                               const Point3D& plane_normal) {
  double distance = (point - plane_point).dot(plane_normal);
  return point - distance * plane_normal;
}

bool RayTriangleIntersection(const Point3D& ray_origin,
                             const Eigen::Vector3d& ray_direction,
                             const Point3D& v0, const Point3D& v1,
                             const Point3D& v2, Point3D* intersection_point) {
  // M?ller?Trumbore intersection algorithm
  const double kEpsilon = 1e-8;
  
  Eigen::Vector3d edge1 = v1 - v0;
  Eigen::Vector3d edge2 = v2 - v0;
  Eigen::Vector3d h = ray_direction.cross(edge2);
  double a = edge1.dot(h);
  
  if (std::abs(a) < kEpsilon) {
    return false;  // Ray is parallel to triangle
  }
  
  double f = 1.0 / a;
  Eigen::Vector3d s = ray_origin - v0;
  double u = f * s.dot(h);
  
  if (u < 0.0 || u > 1.0) {
    return false;
  }
  
  Eigen::Vector3d q = s.cross(edge1);
  double v = f * ray_direction.dot(q);
  
  if (v < 0.0 || u + v > 1.0) {
    return false;
  }
  
  double t = f * edge2.dot(q);
  
  if (t > kEpsilon) {
    if (intersection_point != nullptr) {
      *intersection_point = ray_origin + t * ray_direction;
    }
    return true;
  }
  
  return false;
}

}  // namespace geometry_utils
}  // namespace dental
