// Copyright 2025 Dental Segmentation Project
// Auto Proximal Reconstruction

#ifndef SRC_RECONSTRUCTION_AUTO_PROXIMAL_RECONSTRUCTION_H_
#define SRC_RECONSTRUCTION_AUTO_PROXIMAL_RECONSTRUCTION_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class AutoProximalReconstruction {
 public:
  AutoProximalReconstruction();
  ~AutoProximalReconstruction();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_AUTO_PROXIMAL_RECONSTRUCTION_H_
