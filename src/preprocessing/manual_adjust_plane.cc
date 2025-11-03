// Copyright 2025 Dental Segmentation Project
// Manual adjustment implementation

#include "preprocessing/manual_adjust_plane.h"

#include "common/mesh_utils.h"

namespace dental {
namespace preprocessing {

ManualAdjustPlane::ManualAdjustPlane() {
  // Initialize with identity coordinate system
  coordinate_system_.origin = Point3D::Zero();
  coordinate_system_.x_axis = Eigen::Vector3d::UnitX();
  coordinate_system_.y_axis = Eigen::Vector3d::UnitY();
  coordinate_system_.z_axis = Eigen::Vector3d::UnitZ();
}

ManualAdjustPlane::~ManualAdjustPlane() {}

void ManualAdjustPlane::Initialize(const CoordinateSystem& initial_cs) {
  coordinate_system_ = initial_cs;
}

void ManualAdjustPlane::RotateAroundX(double angle_degrees) {
  double angle_radians = angle_degrees * M_PI / 180.0;
  Eigen::AngleAxisd rotation(angle_radians, coordinate_system_.x_axis);
  
  coordinate_system_.y_axis = rotation * coordinate_system_.y_axis;
  coordinate_system_.z_axis = rotation * coordinate_system_.z_axis;
}

void ManualAdjustPlane::RotateAroundY(double angle_degrees) {
  double angle_radians = angle_degrees * M_PI / 180.0;
  Eigen::AngleAxisd rotation(angle_radians, coordinate_system_.y_axis);
  
  coordinate_system_.x_axis = rotation * coordinate_system_.x_axis;
  coordinate_system_.z_axis = rotation * coordinate_system_.z_axis;
}

void ManualAdjustPlane::RotateAroundZ(double angle_degrees) {
  double angle_radians = angle_degrees * M_PI / 180.0;
  Eigen::AngleAxisd rotation(angle_radians, coordinate_system_.z_axis);
  
  coordinate_system_.x_axis = rotation * coordinate_system_.x_axis;
  coordinate_system_.y_axis = rotation * coordinate_system_.y_axis;
}

void ManualAdjustPlane::Translate(const Eigen::Vector3d& offset) {
  coordinate_system_.origin += offset;
}

Status ManualAdjustPlane::ApplyToMesh(MeshPtr mesh) const {
  if (!mesh || !mesh->IsValid()) {
    return Status::Error(StatusCode::kInvalidInput, "Invalid mesh");
  }
  
  Eigen::Matrix4d transform = coordinate_system_.GetTransformMatrix();
  mesh_utils::TransformMesh(mesh, transform);
  
  return Status::OK();
}

}  // namespace preprocessing
}  // namespace dental
