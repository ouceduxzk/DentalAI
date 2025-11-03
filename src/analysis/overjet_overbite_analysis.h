// Copyright 2025 Dental Segmentation Project
// Overjet Overbite Analysis

#ifndef SRC_ANALYSIS_OVERJET_OVERBITE_ANALYSIS_H_
#define SRC_ANALYSIS_OVERJET_OVERBITE_ANALYSIS_H_

#include <vector>
#include "common/types.h"

namespace dental {
namespace analysis {

class OverjetOverbiteAnalysis {
 public:
  OverjetOverbiteAnalysis();
  ~OverjetOverbiteAnalysis();
  
  Status Analyze(const DentalArchPtr& dental_arch);
  
 private:
};

}  // namespace analysis
}  // namespace dental

#endif  // SRC_ANALYSIS_OVERJET_OVERBITE_ANALYSIS_H_
