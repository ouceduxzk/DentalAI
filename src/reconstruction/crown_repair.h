// Copyright 2025 Dental Segmentation Project
// Crown Repair

#ifndef SRC_RECONSTRUCTION_CROWN_REPAIR_H_
#define SRC_RECONSTRUCTION_CROWN_REPAIR_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class CrownRepair {
 public:
  CrownRepair();
  ~CrownRepair();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_CROWN_REPAIR_H_
