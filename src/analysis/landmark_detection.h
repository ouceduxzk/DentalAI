// Copyright 2025 Dental Segmentation Project
// Landmark Detection

#ifndef SRC_ANALYSIS_LANDMARK_DETECTION_H_
#define SRC_ANALYSIS_LANDMARK_DETECTION_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class LandmarkDetection {
 public:
  LandmarkDetection();
  ~LandmarkDetection();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_LANDMARK_DETECTION_H_
