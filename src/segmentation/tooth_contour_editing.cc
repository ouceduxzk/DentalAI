#include "segmentation/tooth_contour_editing.h"
namespace dental {
namespace segmentation {
ToothContourEditing::ToothContourEditing() {}
ToothContourEditing::~ToothContourEditing() {}
Status ToothContourEditing::EditContour(const std::vector<int>& landmark_indices) {
  return Status::Error(StatusCode::kNotImplemented, "Not implemented");
}
}  // namespace segmentation
}  // namespace dental
