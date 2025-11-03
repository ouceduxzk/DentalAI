// Copyright 2025 Dental Segmentation Project
// Automatic tooth segmentation using AI or traditional methods

#ifndef SRC_SEGMENTATION_AUTO_TOOTH_SEGMENTATION_H_
#define SRC_SEGMENTATION_AUTO_TOOTH_SEGMENTATION_H_

#include <memory>
#include <string>
#include <vector>

#include "common/types.h"

namespace dental {
namespace segmentation {

enum class SegmentationMethod {
  kAI,           // Deep learning-based segmentation
  kClustering    // Traditional hierarchical clustering
};

struct AutoToothSegmentationConfig {
  SegmentationMethod method = SegmentationMethod::kAI;
  
  // AI method config
  std::string model_path;
  
  // Clustering method config
  int max_clusters = 32;
  double curvature_weight = 1.0;
  double normal_weight = 1.0;
  double geodesic_weight = 2.0;  // If manual landmarks provided
  bool use_manual_landmarks = false;
};

class AutoToothSegmentation {
 public:
  AutoToothSegmentation();
  explicit AutoToothSegmentation(const AutoToothSegmentationConfig& config);
  ~AutoToothSegmentation();
  
  // Main segmentation function
  Status Segment(const MeshPtr& input_mesh, 
                 std::vector<ToothPtr>* teeth);
  
  // Set manual landmarks (optional, improves results)
  void SetManualLandmarks(const std::vector<Landmark>& landmarks);
  
  // Configuration
  void SetConfig(const AutoToothSegmentationConfig& config);
  
 private:
  // AI-based segmentation
  Status SegmentUsingAI(const MeshPtr& input_mesh,
                        std::vector<ToothPtr>* teeth);
  
  // Traditional clustering-based segmentation
  Status SegmentUsingClustering(const MeshPtr& input_mesh,
                                std::vector<ToothPtr>* teeth);
  
  // Feature computation for clustering
  struct VertexFeatures {
    double gaussian_curvature;
    double mean_curvature;
    Eigen::Vector3d normal;
    double geodesic_distance_to_landmark;
  };
  
  std::vector<VertexFeatures> ComputeVertexFeatures(const MeshPtr& mesh);
  
  AutoToothSegmentationConfig config_;
  std::vector<Landmark> manual_landmarks_;
};

}  // namespace segmentation
}  // namespace dental

#endif  // SRC_SEGMENTATION_AUTO_TOOTH_SEGMENTATION_H_
