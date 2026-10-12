"""Giới hạn tọa độ và độ cao trong không gian tìm kiếm."""

from dataclasses import dataclass

import numpy as np

from ..constants.network import (
    DEFAULT_AREA_HEIGHT_M,
    DEFAULT_AREA_WIDTH_M,
    DEFAULT_MAX_ALTITUDE_M,
    DEFAULT_MIN_ALTITUDE_M,
)


@dataclass(frozen=True)
class SearchSpace:
    lower_bounds: np.ndarray
    upper_bounds: np.ndarray

    def clip(self, position: np.ndarray) -> np.ndarray:
        return np.clip(position, self.lower_bounds, self.upper_bounds)

    @property
    def dimension(self) -> int:
        return len(self.lower_bounds)


def create_uav_search_space(
    num_uavs: int,
    width: float = DEFAULT_AREA_WIDTH_M,
    height: float = DEFAULT_AREA_HEIGHT_M,
    min_alt: float = DEFAULT_MIN_ALTITUDE_M,
    max_alt: float = DEFAULT_MAX_ALTITUDE_M,
) -> SearchSpace:
    """Tạo không gian tìm kiếm cho num_uavs, mỗi UAV có 3 tọa độ [x, y, z]."""
    lb_single = np.array([0.0, 0.0, min_alt], dtype=float)
    ub_single = np.array([width, height, max_alt], dtype=float)

    lower_bounds = np.tile(lb_single, num_uavs)
    upper_bounds = np.tile(ub_single, num_uavs)

    return SearchSpace(lower_bounds=lower_bounds, upper_bounds=upper_bounds)
