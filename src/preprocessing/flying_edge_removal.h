// Copyright 2025 Dental Segmentation Project
// Remove flying edges, non-manifold elements, and degenerate faces

#ifndef SRC_PREPROCESSING_FLYING_EDGE_REMOVAL_H_
#define SRC_PREPROCESSING_FLYING_EDGE_REMOVAL_H_

#include "common/types.h"

namespace dental {
namespace preprocessing {

struct FlyingEdgeRemovalConfig {
  int max_iterations = 3;
  bool remove_non_connected = true;
  bool remove_non_manifold = true;
  bool remove_degenerate = true;
  bool keep_largest_component_only = true;
};

class FlyingEdgeRemoval {
 public:
  FlyingEdgeRemoval();
  explicit FlyingEdgeRemoval(const FlyingEdgeRemovalConfig& config);
  ~FlyingEdgeRemoval();
  
  // Main processing function
  Status Process(MeshPtr mesh);
  
  // Individual operations
  Status RemoveNonConnectedRegions(MeshPtr mesh);
  Status RemoveNonManifoldElements(MeshPtr mesh);
  Status RemoveDegenerateElements(MeshPtr mesh);
  
  // Configuration
  void SetConfig(const FlyingEdgeRemovalConfig& config);
  
 private:
  FlyingEdgeRemovalConfig config_;
};

}  // namespace preprocessing
}  // namespace dental

#endif  // SRC_PREPROCESSING_FLYING_EDGE_REMOVAL_H_
