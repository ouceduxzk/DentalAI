// Copyright 2025 Dental Segmentation Project
// Angle Classification

#ifndef SRC_ANALYSIS_ANGLE_CLASSIFICATION_H_
#define SRC_ANALYSIS_ANGLE_CLASSIFICATION_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class AngleClassification {
 public:
  AngleClassification();
  ~AngleClassification();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_ANGLE_CLASSIFICATION_H_
