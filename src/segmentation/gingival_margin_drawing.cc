// Copyright 2025 Dental Segmentation Project
// Gingival margin drawing implementation

#include "segmentation/gingival_margin_drawing.h"

#include "common/geometry_utils.h"

namespace dental {
namespace segmentation {

GingivalMarginDrawing::GingivalMarginDrawing() : config_() {}

GingivalMarginDrawing::GingivalMarginDrawing(const GingivalMarginConfig& config)
    : config_(config) {}

GingivalMarginDrawing::~GingivalMarginDrawing() {}

void GingivalMarginDrawing::AddLandmark(const Point3D& point) {
  landmarks_.push_back(point);
}

void GingivalMarginDrawing::ClearLandmarks() {
  landmarks_.clear();
}

Status GingivalMarginDrawing::GenerateCurve(const MeshPtr& mesh,
                                             std::vector<Point3D>* curve_points) {
  if (landmarks_.size() < 2) {
    return Status::Error(StatusCode::kInvalidInput, 
                         "Need at least 2 landmarks");
  }
  
  if (config_.curve_method == CurveMethod::kBSpline) {
    return GenerateBSplineCurve(curve_points);
  } else {
    return GenerateDijkstraCurve(mesh, curve_points);
  }
}

void GingivalMarginDrawing::SetConfig(const GingivalMarginConfig& config) {
  config_ = config;
}

Status GingivalMarginDrawing::GenerateBSplineCurve(
    std::vector<Point3D>* curve_points) {
  
  *curve_points = geometry_utils::FitBSpline(landmarks_, 
                                              config_.bspline_samples);
  
  return Status::OK();
}

Status GingivalMarginDrawing::GenerateDijkstraCurve(
    const MeshPtr& mesh,
    std::vector<Point3D>* curve_points) {
  
  // TODO: Find closest vertices to landmarks and compute shortest paths
  return Status::Error(StatusCode::kNotImplemented, 
                       "Dijkstra curve generation not yet implemented");
}

}  // namespace segmentation
}  // namespace dental
