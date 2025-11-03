// Copyright 2025 Dental Segmentation Project
// Manual adjustment of occlusal plane (GUI-based)

#ifndef SRC_PREPROCESSING_MANUAL_ADJUST_PLANE_H_
#define SRC_PREPROCESSING_MANUAL_ADJUST_PLANE_H_

#include "common/types.h"

namespace dental {
namespace preprocessing {

class ManualAdjustPlane {
 public:
  ManualAdjustPlane();
  ~ManualAdjustPlane();
  
  // Initialize with initial coordinate system
  void Initialize(const CoordinateSystem& initial_cs);
  
  // Manual adjustment operations
  void RotateAroundX(double angle_degrees);
  void RotateAroundY(double angle_degrees);
  void RotateAroundZ(double angle_degrees);
  void Translate(const Eigen::Vector3d& offset);
  
  // Get current coordinate system
  const CoordinateSystem& GetCoordinateSystem() const {
    return coordinate_system_;
  }
  
  // Apply transformation to mesh
  Status ApplyToMesh(MeshPtr mesh) const;
  
 private:
  CoordinateSystem coordinate_system_;
};

}  // namespace preprocessing
}  // namespace dental

#endif  // SRC_PREPROCESSING_MANUAL_ADJUST_PLANE_H_
