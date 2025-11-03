// Copyright 2025 Dental Segmentation Project
// Auto adjust occlusal plane using least squares or SVM fitting and PCA

#ifndef SRC_PREPROCESSING_AUTO_ADJUST_PLANE_H_
#define SRC_PREPROCESSING_AUTO_ADJUST_PLANE_H_

#include "common/types.h"

namespace dental {
namespace preprocessing {

// Configuration for automatic plane adjustment
struct AutoAdjustPlaneConfig {
  enum class FittingMethod {
    kLeastSquares,
    kSVM
  };
  
  FittingMethod fitting_method = FittingMethod::kLeastSquares;
  bool use_pca_for_axes = true;
  double svm_epsilon = 0.1;
  double svm_c_parameter = 1.0;
};

class AutoAdjustPlane {
 public:
  AutoAdjustPlane();
  explicit AutoAdjustPlane(const AutoAdjustPlaneConfig& config);
  ~AutoAdjustPlane();
  
  // Main processing function
  Status Process(const MeshPtr& input_mesh, CoordinateSystem* output_cs);
  
  // Set configuration
  void SetConfig(const AutoAdjustPlaneConfig& config);
  
  // Get last computed coordinate system
  const CoordinateSystem& GetCoordinateSystem() const {
    return coordinate_system_;
  }
  
 private:
  // Fit plane using least squares
  Status FitPlaneLeaseSquares(const std::vector<Point3D>& points,
                               Point3D* plane_point, 
                               Eigen::Vector3d* plane_normal);
  
  // Fit plane using SVM
  Status FitPlaneSVM(const std::vector<Point3D>& points,
                     Point3D* plane_point,
                     Eigen::Vector3d* plane_normal);
  
  // Determine axes using PCA
  Status DetermineAxesUsingPCA(const std::vector<Point3D>& points,
                                const Eigen::Vector3d& z_axis,
                                Eigen::Vector3d* x_axis,
                                Eigen::Vector3d* y_axis);
  
  // Extract boundary points from mesh
  std::vector<Point3D> ExtractBoundaryPoints(const MeshPtr& mesh);
  
  AutoAdjustPlaneConfig config_;
  CoordinateSystem coordinate_system_;
};

}  // namespace preprocessing
}  // namespace dental

#endif  // SRC_PREPROCESSING_AUTO_ADJUST_PLANE_H_
