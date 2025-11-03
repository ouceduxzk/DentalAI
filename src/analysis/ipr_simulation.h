// Copyright 2025 Dental Segmentation Project
// Ipr Simulation

#ifndef SRC_ANALYSIS_IPR_SIMULATION_H_
#define SRC_ANALYSIS_IPR_SIMULATION_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class IprSimulation {
 public:
  IprSimulation();
  ~IprSimulation();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_IPR_SIMULATION_H_
