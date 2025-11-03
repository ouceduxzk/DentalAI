// Copyright 2025 Dental Segmentation Project
// Spee Curve Analysis

#ifndef SRC_ANALYSIS_SPEE_CURVE_ANALYSIS_H_
#define SRC_ANALYSIS_SPEE_CURVE_ANALYSIS_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class SpeeCurveAnalysis {
 public:
  SpeeCurveAnalysis();
  ~SpeeCurveAnalysis();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_SPEE_CURVE_ANALYSIS_H_
