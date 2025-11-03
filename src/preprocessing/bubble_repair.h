// Copyright 2025 Dental Segmentation Project
// Bubble repair using Laplacian smoothing

#ifndef SRC_PREPROCESSING_BUBBLE_REPAIR_H_
#define SRC_PREPROCESSING_BUBBLE_REPAIR_H_

#include <vector>

#include "common/types.h"

namespace dental {
namespace preprocessing {

struct BubbleRepairConfig {
  int smoothing_iterations = 10;
  double lambda = 0.5;  // Smoothing factor
  bool auto_detect_bubbles = false;
  double bubble_threshold = 0.1;  // For auto-detection
};

class BubbleRepair {
 public:
  BubbleRepair();
  explicit BubbleRepair(const BubbleRepairConfig& config);
  ~BubbleRepair();
  
  // Repair bubble with manually selected boundary
  Status RepairManual(MeshPtr mesh, 
                      const std::vector<int>& boundary_vertex_indices);
  
  // Auto-detect and repair bubbles
  Status RepairAuto(MeshPtr mesh);
  
  // Configuration
  void SetConfig(const BubbleRepairConfig& config);
  
 private:
  // Detect bubbles automatically
  std::vector<std::vector<int>> DetectBubbles(const MeshPtr& mesh);
  
  // Apply Laplacian smoothing to region
  Status ApplyLaplacianSmoothing(MeshPtr mesh,
                                  const std::vector<int>& region_indices,
                                  const std::vector<int>& boundary_indices);
  
  BubbleRepairConfig config_;
};

}  // namespace preprocessing
}  // namespace dental

#endif  // SRC_PREPROCESSING_BUBBLE_REPAIR_H_
