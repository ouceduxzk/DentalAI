// Copyright 2025 Dental Segmentation Project
// Automatic tooth segmentation implementation

#include "segmentation/auto_tooth_segmentation.h"

#include "common/geometry_utils.h"

namespace dental {
namespace segmentation {

AutoToothSegmentation::AutoToothSegmentation() : config_() {}

AutoToothSegmentation::AutoToothSegmentation(
    const AutoToothSegmentationConfig& config)
    : config_(config) {}

AutoToothSegmentation::~AutoToothSegmentation() {}

Status AutoToothSegmentation::Segment(const MeshPtr& input_mesh,
                                       std::vector<ToothPtr>* teeth) {
  if (!input_mesh || !input_mesh->IsValid()) {
    return Status::Error(StatusCode::kInvalidInput, "Invalid input mesh");
  }
  
  if (config_.method == SegmentationMethod::kAI) {
    return SegmentUsingAI(input_mesh, teeth);
  } else {
    return SegmentUsingClustering(input_mesh, teeth);
  }
}

void AutoToothSegmentation::SetManualLandmarks(
    const std::vector<Landmark>& landmarks) {
  manual_landmarks_ = landmarks;
  config_.use_manual_landmarks = !landmarks.empty();
}

void AutoToothSegmentation::SetConfig(
    const AutoToothSegmentationConfig& config) {
  config_ = config;
}

Status AutoToothSegmentation::SegmentUsingAI(const MeshPtr& input_mesh,
                                              std::vector<ToothPtr>* teeth) {
  // TODO: Load AI model and perform inference
  // This would typically use ONNX Runtime or TensorFlow C++ API
  return Status::Error(StatusCode::kNotImplemented, 
                       "AI segmentation not yet implemented");
}

Status AutoToothSegmentation::SegmentUsingClustering(
    const MeshPtr& input_mesh,
                                              std::vector<ToothPtr>* teeth) {
  // Compute vertex features
  std::vector<VertexFeatures> features = ComputeVertexFeatures(input_mesh);
  
  // TODO: Implement hierarchical clustering based on features
  // 1. Compute similarity matrix
  // 2. Iterative region growing and merging
  // 3. Split clusters into individual teeth
  
  return Status::Error(StatusCode::kNotImplemented, 
                       "Clustering segmentation not yet implemented");
}

std::vector<AutoToothSegmentation::VertexFeatures> 
AutoToothSegmentation::ComputeVertexFeatures(const MeshPtr& mesh) {
  std::vector<VertexFeatures> features(mesh->GetVertexCount());
  
  for (size_t i = 0; i < mesh->GetVertexCount(); ++i) {
    features[i].gaussian_curvature = 
        geometry_utils::ComputeGaussianCurvature(mesh, i);
    features[i].mean_curvature = 
        geometry_utils::ComputeMeanCurvature(mesh, i);
    features[i].normal = mesh->vertices[i].normal;
    features[i].geodesic_distance_to_landmark = 0.0;  // TODO: Compute if needed
  }
  
  return features;
}

}  // namespace segmentation
}  // namespace dental
