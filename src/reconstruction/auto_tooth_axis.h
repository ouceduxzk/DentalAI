// Copyright 2025 Dental Segmentation Project
// Auto Tooth Axis

#ifndef SRC_RECONSTRUCTION_AUTO_TOOTH_AXIS_H_
#define SRC_RECONSTRUCTION_AUTO_TOOTH_AXIS_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class AutoToothAxis {
 public:
  AutoToothAxis();
  ~AutoToothAxis();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_AUTO_TOOTH_AXIS_H_
