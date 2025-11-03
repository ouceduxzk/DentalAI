// Copyright 2025 Dental Segmentation Project
// Depression repair (similar to bubble repair)

#ifndef SRC_PREPROCESSING_DEPRESSION_REPAIR_H_
#define SRC_PREPROCESSING_DEPRESSION_REPAIR_H_

#include "preprocessing/bubble_repair.h"

namespace dental {
namespace preprocessing {

// Depression repair uses the same approach as bubble repair
using DepressionRepairConfig = BubbleRepairConfig;
using DepressionRepair = BubbleRepair;

}  // namespace preprocessing
}  // namespace dental

#endif  // SRC_PREPROCESSING_DEPRESSION_REPAIR_H_
