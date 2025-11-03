// Copyright 2025 Dental Segmentation Project
// Mesh utility functions

#ifndef SRC_COMMON_MESH_UTILS_H_
#define SRC_COMMON_MESH_UTILS_H_

#include <string>
#include <vector>

#include "common/types.h"

namespace dental {
namespace mesh_utils {

// Load mesh from file (STL, OBJ, PLY)
Status LoadMesh(const std::string& filename, MeshPtr* mesh);

// Save mesh to file
Status SaveMesh(const std::string& filename, const MeshPtr& mesh);

// Compute mesh normals
void ComputeVertexNormals(MeshPtr mesh);
void ComputeFaceNormals(MeshPtr mesh);

// Mesh quality checks
bool HasNonManifoldEdges(const MeshPtr& mesh);
bool HasDegenerateTriangles(const MeshPtr& mesh);
std::vector<int> FindConnectedComponents(const MeshPtr& mesh);

// Mesh repair operations
Status RemoveNonManifoldElements(MeshPtr mesh);
Status RemoveDegenerateTriangles(MeshPtr mesh);
Status KeepLargestComponent(MeshPtr mesh);

// Mesh smoothing
Status LaplacianSmooth(MeshPtr mesh, int iterations, double lambda);

// Mesh transformations
void TransformMesh(MeshPtr mesh, const Eigen::Matrix4d& transform);
void CenterMesh(MeshPtr mesh);
void ScaleMesh(MeshPtr mesh, double scale);

// Bounding box
struct BoundingBox {
  Point3D min_corner;
  Point3D max_corner;
  
  Point3D GetCenter() const;
  Point3D GetSize() const;
};

BoundingBox ComputeBoundingBox(const MeshPtr& mesh);

}  // namespace mesh_utils
}  // namespace dental

#endif  // SRC_COMMON_MESH_UTILS_H_
