// Copyright 2025 Dental Segmentation Project
// Mesh With Gingiva Exporter

#ifndef SRC_OUTPUT_MESH_WITH_GINGIVA_EXPORTER_H_
#define SRC_OUTPUT_MESH_WITH_GINGIVA_EXPORTER_H_

#include <string>
#include "common/types.h"

namespace dental {
namespace output {

enum class ExportFormat {
  kSTL,
  kOBJ,
  kPLY,
  kOFF
};

class MeshWithGingivaExporter {
 public:
  MeshWithGingivaExporter();
  ~MeshWithGingivaExporter();
  
  Status Export(const std::string& filename, 
                const MeshPtr& mesh,
                ExportFormat format = ExportFormat::kSTL);
  
 private:
  Status ExportSTL(const std::string& filename, const MeshPtr& mesh);
  Status ExportOBJ(const std::string& filename, const MeshPtr& mesh);
  Status ExportPLY(const std::string& filename, const MeshPtr& mesh);
  Status ExportOFF(const std::string& filename, const MeshPtr& mesh);
};

}  // namespace output
}  // namespace dental

#endif  // SRC_OUTPUT_MESH_WITH_GINGIVA_EXPORTER_H_
