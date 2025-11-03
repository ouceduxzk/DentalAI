// Copyright 2025 Dental Segmentation Project
// Flying edge removal implementation

#include "preprocessing/flying_edge_removal.h"

#include "common/mesh_utils.h"

namespace dental {
namespace preprocessing {

FlyingEdgeRemoval::FlyingEdgeRemoval() : config_() {}

FlyingEdgeRemoval::FlyingEdgeRemoval(const FlyingEdgeRemovalConfig& config)
    : config_(config) {}

FlyingEdgeRemoval::~FlyingEdgeRemoval() {}

Status FlyingEdgeRemoval::Process(MeshPtr mesh) {
  if (!mesh || !mesh->IsValid()) {
    return Status::Error(StatusCode::kInvalidInput, "Invalid mesh");
  }
  
  Status status;
  
  for (int iter = 0; iter < config_.max_iterations; ++iter) {
    bool modified = false;
    
    // Remove non-connected regions
    if (config_.remove_non_connected) {
      if (config_.keep_largest_component_only) {
        status = mesh_utils::KeepLargestComponent(mesh);
        if (!status.Ok()) return status;
        modified = true;
      }
    }
    
    // Remove non-manifold elements
    if (config_.remove_non_manifold) {
      status = RemoveNonManifoldElements(mesh);
      if (!status.Ok()) return status;
      if (mesh_utils::HasNonManifoldEdges(mesh)) {
        modified = true;
      }
    }
    
    // Remove degenerate elements
    if (config_.remove_degenerate) {
      status = RemoveDegenerateElements(mesh);
      if (!status.Ok()) return status;
      if (mesh_utils::HasDegenerateTriangles(mesh)) {
        modified = true;
      }
    }
    
    // If nothing was modified, we're done
    if (!modified) {
      break;
    }
  }
  
  return Status::OK();
}

Status FlyingEdgeRemoval::RemoveNonConnectedRegions(MeshPtr mesh) {
  return mesh_utils::KeepLargestComponent(mesh);
}

Status FlyingEdgeRemoval::RemoveNonManifoldElements(MeshPtr mesh) {
  return mesh_utils::RemoveNonManifoldElements(mesh);
}

Status FlyingEdgeRemoval::RemoveDegenerateElements(MeshPtr mesh) {
  return mesh_utils::RemoveDegenerateTriangles(mesh);
}

void FlyingEdgeRemoval::SetConfig(const FlyingEdgeRemovalConfig& config) {
  config_ = config;
}

}  // namespace preprocessing
}  // namespace dental
