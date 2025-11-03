// Copyright 2025 Dental Segmentation Project
// Arch Curve Analysis

#ifndef SRC_ANALYSIS_ARCH_CURVE_ANALYSIS_H_
#define SRC_ANALYSIS_ARCH_CURVE_ANALYSIS_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class ArchCurveAnalysis {
 public:
  ArchCurveAnalysis();
  ~ArchCurveAnalysis();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_ARCH_CURVE_ANALYSIS_H_
