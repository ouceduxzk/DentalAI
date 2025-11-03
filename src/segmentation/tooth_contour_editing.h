// Copyright 2025 Dental Segmentation Project
#ifndef SRC_SEGMENTATION_TOOTH_CONTOUR_EDITING_H_
#define SRC_SEGMENTATION_TOOTH_CONTOUR_EDITING_H_
#include "common/types.h"
namespace dental {
namespace segmentation {
class ToothContourEditing {
 public:
  ToothContourEditing();
  ~ToothContourEditing();
  Status EditContour(const std::vector<int>& landmark_indices);
 private:
};
}  // namespace segmentation
}  // namespace dental
#endif
