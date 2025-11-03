// Copyright 2025 Dental Segmentation Project
// Root Simulation

#ifndef SRC_RECONSTRUCTION_ROOT_SIMULATION_H_
#define SRC_RECONSTRUCTION_ROOT_SIMULATION_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class RootSimulation {
 public:
  RootSimulation();
  ~RootSimulation();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_ROOT_SIMULATION_H_
