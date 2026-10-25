"""Lớp định nghĩa bài toán tối ưu vị trí UAV (Problem Formulation)."""

import numpy as np

from ..constants.network import (
    DEFAULT_AREA_HEIGHT_M,
    DEFAULT_AREA_WIDTH_M,
    DEFAULT_MAX_ALTITUDE_M,
    DEFAULT_MIN_ALTITUDE_M,
    DEFAULT_NUM_UAVS,
    SNR_THRESHOLD_DB,
    WEIGHT_COVERAGE,
    WEIGHT_ENERGY,
    WEIGHT_INTERFERENCE,
)
from ..objectives.metrics import ObjectiveValues, evaluate_solution
from .search_space import SearchSpace, create_uav_search_space
from .solution_encoding import decode_uav_positions


class UAVPlacementProblem:
    """Bài toán tối ưu hóa vị trí không gian 3D của N UAVs để phục vụ M UEs."""

    def __init__(
        self,
        ue_coords: np.ndarray,
        num_uavs: int = DEFAULT_NUM_UAVS,
        area_width: float = DEFAULT_AREA_WIDTH_M,
        area_height: float = DEFAULT_AREA_HEIGHT_M,
        min_altitude: float = DEFAULT_MIN_ALTITUDE_M,
        max_altitude: float = DEFAULT_MAX_ALTITUDE_M,
        snr_threshold: float = SNR_THRESHOLD_DB,
        weight_coverage: float = WEIGHT_COVERAGE,
        weight_energy: float = WEIGHT_ENERGY,
        weight_interference: float = WEIGHT_INTERFERENCE,
        min_uav_distance: float = 10.0,
    ):
        if ue_coords.ndim != 2 or ue_coords.shape[1] != 3:
            raise ValueError(f"ue_coords phải có shape (M, 3), nhận được: {ue_coords.shape}")

        self.ue_coords = np.asarray(ue_coords, dtype=float)
        if self.ue_coords.shape[0] == 0:
            raise ValueError("ue_coords phải chứa ít nhất một user.")
        if not np.isfinite(self.ue_coords).all():
            raise ValueError("ue_coords chỉ được chứa các giá trị số hữu hạn.")
        if not isinstance(num_uavs, (int, np.integer)) or num_uavs <= 0:
            raise ValueError("num_uavs must be a positive integer")
        if not np.isfinite([area_width, area_height, min_altitude, max_altitude, min_uav_distance]).all():
            raise ValueError("Bounds and minimum distance must be finite")
        if area_width <= 0 or area_height <= 0 or max_altitude <= min_altitude or min_uav_distance < 0:
            raise ValueError("Invalid bounds or minimum distance")
        self.min_altitude = min_altitude
        self.max_altitude = max_altitude
        self.min_uav_distance = min_uav_distance
        self.num_uavs = num_uavs
        self.snr_threshold = snr_threshold
        self.weights = (weight_coverage, weight_energy, weight_interference)

        self.search_space = create_uav_search_space(
            num_uavs=num_uavs,
            width=area_width,
            height=area_height,
            min_alt=min_altitude,
            max_alt=max_altitude,
        )
        self.dimension = self.search_space.dimension

    def evaluate(self, solution: np.ndarray) -> float:
        """Đánh giá nghiệm và trả về giá trị Fitness (Càng lớn càng tốt).

        Parameters
        ----------
        solution : np.ndarray, shape (num_uavs * 3,)
            Vector phẳng [x1, y1, z1, ..., xN, yN, zN].

        Returns
        -------
        float : Điểm Fitness (Cần tối đa hóa).
        """
        solution = self._validate_solution(solution)
        clipped_solution = self.search_space.clip(solution)
        uav_coords = decode_uav_positions(clipped_solution)
        if not self.is_feasible(clipped_solution):
            return float("-inf")
        w1, w2, w3 = self.weights

        res = evaluate_solution(
            uav_coords=uav_coords,
            ue_coords=self.ue_coords,
            snr_th=self.snr_threshold,
            w1=w1,
            w2=w2,
            w3=w3,
            min_alt=self.min_altitude,
            max_alt=self.max_altitude,
        )
        return res.fitness

    def evaluate_detailed(self, solution: np.ndarray) -> ObjectiveValues:
        """Trả về chi tiết các chỉ số f1, f2, f3 và số lượng UE được phủ."""
        solution = self._validate_solution(solution)
        clipped_solution = self.search_space.clip(solution)
        uav_coords = decode_uav_positions(clipped_solution)
        if not self.is_feasible(clipped_solution):
            raise ValueError("Infeasible placement: minimum UAV separation violated")
        w1, w2, w3 = self.weights

        return evaluate_solution(
            uav_coords=uav_coords,
            ue_coords=self.ue_coords,
            snr_th=self.snr_threshold,
            w1=w1,
            w2=w2,
            w3=w3,
            min_alt=self.min_altitude,
            max_alt=self.max_altitude,
        )

    def _validate_solution(self, solution: np.ndarray) -> np.ndarray:
        solution = np.asarray(solution, dtype=float)
        if solution.shape != (self.dimension,) or not np.isfinite(solution).all():
            raise ValueError(f"solution must have shape ({self.dimension},) and finite values")
        return solution

    def is_feasible(self, solution: np.ndarray) -> bool:
        """Check original bounds and separation without repairing the placement."""
        from .constraints import satisfies_minimum_separation
        solution = self._validate_solution(solution)
        if np.any(solution < self.search_space.lower_bounds) or np.any(solution > self.search_space.upper_bounds):
            return False
        return satisfies_minimum_separation(decode_uav_positions(solution), self.min_uav_distance)
