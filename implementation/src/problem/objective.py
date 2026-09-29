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
    ):
        if ue_coords.ndim != 2 or ue_coords.shape[1] != 3:
            raise ValueError(f"ue_coords phải có shape (M, 3), nhận được: {ue_coords.shape}")

        self.ue_coords = np.asarray(ue_coords, dtype=float)
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
        clipped_solution = self.search_space.clip(solution)
        uav_coords = decode_uav_positions(clipped_solution)
        w1, w2, w3 = self.weights

        res = evaluate_solution(
            uav_coords=uav_coords,
            ue_coords=self.ue_coords,
            snr_th=self.snr_threshold,
            w1=w1,
            w2=w2,
            w3=w3,
        )
        return res.fitness

    def evaluate_detailed(self, solution: np.ndarray) -> ObjectiveValues:
        """Trả về chi tiết các chỉ số f1, f2, f3 và số lượng UE được phủ."""
        clipped_solution = self.search_space.clip(solution)
        uav_coords = decode_uav_positions(clipped_solution)
        w1, w2, w3 = self.weights

        return evaluate_solution(
            uav_coords=uav_coords,
            ue_coords=self.ue_coords,
            snr_th=self.snr_threshold,
            w1=w1,
            w2=w2,
            w3=w3,
        )
