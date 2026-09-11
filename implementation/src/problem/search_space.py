"""Giới hạn tọa độ và độ cao trong không gian tìm kiếm."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class SearchSpace:
    lower_bounds: np.ndarray
    upper_bounds: np.ndarray

    def clip(self, position: np.ndarray) -> np.ndarray:
        return np.clip(position, self.lower_bounds, self.upper_bounds)
