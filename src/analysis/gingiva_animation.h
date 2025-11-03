// Copyright 2025 Dental Segmentation Project
// Gingiva Animation

#ifndef SRC_ANALYSIS_GINGIVA_ANIMATION_H_
#define SRC_ANALYSIS_GINGIVA_ANIMATION_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class GingivaAnimation {
 public:
  GingivaAnimation();
  ~GingivaAnimation();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_GINGIVA_ANIMATION_H_
