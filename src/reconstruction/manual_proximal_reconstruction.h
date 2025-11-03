// Copyright 2025 Dental Segmentation Project
// Manual Proximal Reconstruction

#ifndef SRC_RECONSTRUCTION_MANUAL_PROXIMAL_RECONSTRUCTION_H_
#define SRC_RECONSTRUCTION_MANUAL_PROXIMAL_RECONSTRUCTION_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class ManualProximalReconstruction {
 public:
  ManualProximalReconstruction();
  ~ManualProximalReconstruction();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_MANUAL_PROXIMAL_RECONSTRUCTION_H_
