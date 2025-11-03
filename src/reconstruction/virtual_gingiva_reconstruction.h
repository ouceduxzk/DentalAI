// Copyright 2025 Dental Segmentation Project
// Virtual Gingiva Reconstruction

#ifndef SRC_RECONSTRUCTION_VIRTUAL_GINGIVA_RECONSTRUCTION_H_
#define SRC_RECONSTRUCTION_VIRTUAL_GINGIVA_RECONSTRUCTION_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class VirtualGingivaReconstruction {
 public:
  VirtualGingivaReconstruction();
  ~VirtualGingivaReconstruction();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_VIRTUAL_GINGIVA_RECONSTRUCTION_H_
