// Copyright 2025 Dental Segmentation Project
// Common types implementation

#include "common/types.h"

namespace dental {

void Mesh::Clear() {
  vertices.clear();
  faces.clear();
}

bool Mesh::IsValid() const {
  if (vertices.empty() || faces.empty()) {
    return false;
  }
  
  // Check if all face indices are valid
  for (const auto& face : faces) {
    for (int idx : face.vertex_indices) {
      if (idx < 0 || idx >= static_cast<int>(vertices.size())) {
        return false;
      }
    }
  }
  
  return true;
}

Eigen::Matrix4d CoordinateSystem::GetTransformMatrix() const {
  Eigen::Matrix4d transform = Eigen::Matrix4d::Identity();
  transform.block<3, 1>(0, 0) = x_axis;
  transform.block<3, 1>(0, 1) = y_axis;
  transform.block<3, 1>(0, 2) = z_axis;
  transform.block<3, 1>(0, 3) = origin;
  return transform;
}

}  // namespace dental
