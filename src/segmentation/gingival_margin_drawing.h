// Copyright 2025 Dental Segmentation Project
// Gingival margin line drawing using B-spline or Dijkstra shortest path

#ifndef SRC_SEGMENTATION_GINGIVAL_MARGIN_DRAWING_H_
#define SRC_SEGMENTATION_GINGIVAL_MARGIN_DRAWING_H_

#include <vector>

#include "common/types.h"

namespace dental {
namespace segmentation {

enum class CurveMethod {
  kBSpline,
  kDijkstraShortestPath
};

struct GingivalMarginConfig {
  CurveMethod curve_method = CurveMethod::kBSpline;
  int bspline_degree = 3;
  int bspline_samples = 100;
};

class GingivalMarginDrawing {
 public:
  GingivalMarginDrawing();
  explicit GingivalMarginDrawing(const GingivalMarginConfig& config);
  ~GingivalMarginDrawing();
  
  // Add landmark point
  void AddLandmark(const Point3D& point);
  void ClearLandmarks();
  
  // Generate curve through landmarks
  Status GenerateCurve(const MeshPtr& mesh, 
                       std::vector<Point3D>* curve_points);
  
  // Configuration
  void SetConfig(const GingivalMarginConfig& config);
  
 private:
  Status GenerateBSplineCurve(std::vector<Point3D>* curve_points);
  Status GenerateDijkstraCurve(const MeshPtr& mesh,
                                std::vector<Point3D>* curve_points);
  
  GingivalMarginConfig config_;
  std::vector<Point3D> landmarks_;
};

}  // namespace segmentation
}  // namespace dental

#endif  // SRC_SEGMENTATION_GINGIVAL_MARGIN_DRAWING_H_
