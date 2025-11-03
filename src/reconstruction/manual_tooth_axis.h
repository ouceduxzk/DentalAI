// Copyright 2025 Dental Segmentation Project
// Manual Tooth Axis

#ifndef SRC_RECONSTRUCTION_MANUAL_TOOTH_AXIS_H_
#define SRC_RECONSTRUCTION_MANUAL_TOOTH_AXIS_H_

#include "common/types.h"

namespace dental {
namespace reconstruction {

class ManualToothAxis {
 public:
  ManualToothAxis();
  ~ManualToothAxis();
  
  Status Process(const MeshPtr& input_mesh);
  
 private:
};

}  // namespace reconstruction
}  // namespace dental

#endif  // SRC_RECONSTRUCTION_MANUAL_TOOTH_AXIS_H_
