// Copyright 2025 Dental Segmentation Project
// Auto adjust occlusal plane implementation

#include "preprocessing/auto_adjust_plane.h"

#include "common/geometry_utils.h"

namespace dental {
namespace preprocessing {

AutoAdjustPlane::AutoAdjustPlane() : config_() {}

AutoAdjustPlane::AutoAdjustPlane(const AutoAdjustPlaneConfig& config)
    : config_(config) {}

AutoAdjustPlane::~AutoAdjustPlane() {}

Status AutoAdjustPlane::Process(const MeshPtr& input_mesh,
                                 CoordinateSystem* output_cs) {
  if (!input_mesh || !input_mesh->IsValid()) {
    return Status::Error(StatusCode::kInvalidInput, "Invalid input mesh");
  }
  
  // Extract boundary points
  std::vector<Point3D> boundary_points = ExtractBoundaryPoints(input_mesh);
  if (boundary_points.empty()) {
    return Status::Error(StatusCode::kProcessingError, 
                         "Failed to extract boundary points");
  }
  
  // Fit plane to determine Z direction
  Point3D plane_point;
  Eigen::Vector3d z_axis;
  
  Status status;
  if (config_.fitting_method == AutoAdjustPlaneConfig::FittingMethod::kLeastSquares) {
    status = FitPlaneLeaseSquares(boundary_points, &plane_point, &z_axis);
  } else {
    status = FitPlaneSVM(boundary_points, &plane_point, &z_axis);
  }
  
  if (!status.Ok()) {
    return status;
  }
  
  // Determine X and Y axes
  Eigen::Vector3d x_axis, y_axis;
  if (config_.use_pca_for_axes) {
    status = DetermineAxesUsingPCA(boundary_points, z_axis, &x_axis, &y_axis);
    if (!status.Ok()) {
      return status;
    }
  } else {
    // Default orthogonal axes
    x_axis = Eigen::Vector3d::UnitX();
    y_axis = z_axis.cross(x_axis).normalized();
    x_axis = y_axis.cross(z_axis).normalized();
  }
  
  // Construct coordinate system
  coordinate_system_.origin = plane_point;
  coordinate_system_.x_axis = x_axis;
  coordinate_system_.y_axis = y_axis;
  coordinate_system_.z_axis = z_axis;
  
  if (output_cs != nullptr) {
    *output_cs = coordinate_system_;
  }
  
  return Status::OK();
}

void AutoAdjustPlane::SetConfig(const AutoAdjustPlaneConfig& config) {
  config_ = config;
}

Status AutoAdjustPlane::FitPlaneLeaseSquares(
    const std::vector<Point3D>& points,
    Point3D* plane_point, 
    Eigen::Vector3d* plane_normal) {
  
  if (points.size() < 3) {
    return Status::Error(StatusCode::kInvalidInput, 
                         "Need at least 3 points for plane fitting");
  }
  
  // Compute centroid
  Point3D centroid = Point3D::Zero();
  for (const auto& p : points) {
    centroid += p;
  }
  centroid /= static_cast<double>(points.size());
  
  // Build covariance matrix
  Eigen::Matrix3d covariance = Eigen::Matrix3d::Zero();
  for (const auto& p : points) {
    Point3D centered = p - centroid;
    covariance += centered * centered.transpose();
  }
  
  // Compute eigenvectors - normal is eigenvector with smallest eigenvalue
  Eigen::SelfAdjointEigenSolver<Eigen::Matrix3d> solver(covariance);
  *plane_normal = solver.eigenvectors().col(0);
  *plane_point = centroid;
  
  return Status::OK();
}

Status AutoAdjustPlane::FitPlaneSVM(const std::vector<Point3D>& points,
                                     Point3D* plane_point,
                                     Eigen::Vector3d* plane_normal) {
  // TODO: Implement SVM-based plane fitting
  // For now, fall back to least squares
  return FitPlaneLeaseSquares(points, plane_point, plane_normal);
}

Status AutoAdjustPlane::DetermineAxesUsingPCA(
    const std::vector<Point3D>& points,
    const Eigen::Vector3d& z_axis,
    Eigen::Vector3d* x_axis,
    Eigen::Vector3d* y_axis) {
  
  // Use PCA to find principal directions
  geometry_utils::PCAResult pca = geometry_utils::ComputePCA(points);
  
  // Choose X axis as the principal direction most perpendicular to Z
  double dot1 = std::abs(pca.principal_axis1.dot(z_axis));
  double dot2 = std::abs(pca.principal_axis2.dot(z_axis));
  
  if (dot1 < dot2) {
    *x_axis = pca.principal_axis1;
  } else {
    *x_axis = pca.principal_axis2;
  }
  
  // Y axis is perpendicular to both Z and X
  *y_axis = z_axis.cross(*x_axis).normalized();
  *x_axis = y_axis->cross(z_axis).normalized();
  
  return Status::OK();
}

std::vector<Point3D> AutoAdjustPlane::ExtractBoundaryPoints(
    const MeshPtr& mesh) {
  std::vector<Point3D> boundary_points;
  
  // TODO: Implement intelligent boundary point extraction
  // For now, just sample all vertices
  for (const auto& vertex : mesh->vertices) {
    boundary_points.push_back(vertex.position);
  }
  
  return boundary_points;
}

}  // namespace preprocessing
}  // namespace dental
