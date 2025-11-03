// Copyright 2025 Dental Segmentation Project
// Common types and data structures

#ifndef SRC_COMMON_TYPES_H_
#define SRC_COMMON_TYPES_H_

#include <memory>
#include <string>
#include <vector>

#include <Eigen/Core>
#include <Eigen/Geometry>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

namespace dental {

// Point types
using Point3D = Eigen::Vector3d;
using Point2D = Eigen::Vector2d;
using PointCloud = pcl::PointCloud<pcl::PointXYZ>;
using PointCloudPtr = PointCloud::Ptr;

// Mesh structure
struct Vertex {
  Point3D position;
  Point3D normal;
  int id;
};

struct Face {
  std::vector<int> vertex_indices;
  Point3D normal;
};

struct Mesh {
  std::vector<Vertex> vertices;
  std::vector<Face> faces;
  
  void Clear();
  bool IsValid() const;
  size_t GetVertexCount() const { return vertices.size(); }
  size_t GetFaceCount() const { return faces.size(); }
};

using MeshPtr = std::shared_ptr<Mesh>;

// Tooth structure
struct Tooth {
  int id;  // FDI numbering system
  MeshPtr mesh;
  Point3D center;
  Eigen::Vector3d axis;
  std::vector<int> landmark_ids;
};

using ToothPtr = std::shared_ptr<Tooth>;

// Dental arch structure
struct DentalArch {
  std::vector<ToothPtr> teeth;
  MeshPtr gingiva_mesh;
  std::string arch_type;  // "upper" or "lower"
};

using DentalArchPtr = std::shared_ptr<DentalArch>;

// Coordinate system
struct CoordinateSystem {
  Point3D origin;
  Eigen::Vector3d x_axis;
  Eigen::Vector3d y_axis;
  Eigen::Vector3d z_axis;
  
  Eigen::Matrix4d GetTransformMatrix() const;
};

// Feature point types
enum class LandmarkType {
  kCusp,
  kGingivalMargin,
  kProximalContact,
  kCentroid,
  kOther
};

struct Landmark {
  int id;
  Point3D position;
  LandmarkType type;
  int associated_tooth_id;
};

// Error codes
enum class StatusCode {
  kOk = 0,
  kInvalidInput,
  kProcessingError,
  kFileIOError,
  kNotImplemented
};

struct Status {
  StatusCode code;
  std::string message;
  
  bool Ok() const { return code == StatusCode::kOk; }
  static Status OK() { return {StatusCode::kOk, ""}; }
  static Status Error(StatusCode code, const std::string& msg) {
    return {code, msg};
  }
};

}  // namespace dental

#endif  // SRC_COMMON_TYPES_H_
