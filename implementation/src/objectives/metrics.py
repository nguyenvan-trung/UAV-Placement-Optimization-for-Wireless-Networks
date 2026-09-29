"""Các hàm mục tiêu và hàm thích nghi (Fitness) của hệ thống UAV."""

from typing import NamedTuple

import numpy as np

from ..constants.network import (
    DEFAULT_MAX_ALTITUDE_M,
    DEFAULT_MIN_ALTITUDE_M,
    DEFAULT_P_HOVER_BASE_W,
    DEFAULT_P_TRANSMIT_W,
    SNR_THRESHOLD_DB,
    WEIGHT_COVERAGE,
    WEIGHT_ENERGY,
    WEIGHT_INTERFERENCE,
)
from ..physics.channel import (
    compute_distance_3d,
    compute_elevation_angle_deg,
    compute_los_probability,
    compute_path_loss,
    compute_snr,
)


class ObjectiveValues(NamedTuple):
    fitness: float
    coverage_rate: float       # f1 (càng cao càng tốt)
    energy_normalized: float   # f2 (càng thấp càng tốt)
    interference_rate: float   # f3 (càng thấp càng tốt)
    covered_users_count: int
    total_users_count: int


def calculate_coverage_rate(
    snr_matrix: np.ndarray, snr_th: float = SNR_THRESHOLD_DB
) -> tuple[float, np.ndarray]:
    """Tính tỷ lệ phủ sóng f1.

    Parameters
    ----------
    snr_matrix : np.ndarray, shape (N, M)
        SNR của N UAV tới M người dùng.

    Returns
    -------
    coverage_rate : float
        Tỷ lệ người dùng có ít nhất 1 UAV đạt SNR >= snr_th.
    covered_mask : np.ndarray, shape (M,)
        Boolean mask người dùng nào được phủ.
    """
    is_connected = snr_matrix >= snr_th  # (N, M)
    covered_mask = np.any(is_connected, axis=0)  # (M,)
    coverage_rate = float(np.mean(covered_mask))
    return coverage_rate, covered_mask


def calculate_energy_consumption(
    uav_coords: np.ndarray,
    min_alt: float = DEFAULT_MIN_ALTITUDE_M,
    max_alt: float = DEFAULT_MAX_ALTITUDE_M,
    p_hover_base: float = DEFAULT_P_HOVER_BASE_W,
    p_tx: float = DEFAULT_P_TRANSMIT_W,
) -> float:
    """Tính chỉ số năng lượng tiêu thụ f2 (chuẩn hóa về [0, 1]).

    Công suất bay lơ lửng tăng theo độ cao z.
    f2 = Trung bình tỷ lệ năng lượng của các UAV so với mức tối đa.
    """
    altitudes = uav_coords[:, 2]
    # Hệ số độ cao [0, 1]
    alt_ratio = np.clip((altitudes - min_alt) / (max_alt - min_alt + 1e-6), 0.0, 1.0)
    # Công suất nâng tỷ lệ thuận với độ cao (thêm tối đa 50% công suất ở max_alt)
    p_hover = p_hover_base * (1.0 + 0.5 * alt_ratio)
    p_total = p_hover + p_tx
    p_max = p_hover_base * 1.5 + p_tx
    # Chuẩn hóa về [0, 1]
    f2 = float(np.mean(p_total) / p_max)
    return f2


def calculate_interference_rate(
    snr_matrix: np.ndarray, snr_th: float = SNR_THRESHOLD_DB
) -> float:
    """Tính tỷ lệ nhiễu chồng lấn f3.

    f3 là tỷ lệ người dùng nhận tín hiệu mạnh từ >= 2 UAV cùng lúc.
    """
    connected_uav_count = np.sum(snr_matrix >= snr_th, axis=0)  # (M,)
    interfered_mask = connected_uav_count >= 2
    return float(np.mean(interfered_mask))


def evaluate_solution(
    uav_coords: np.ndarray,
    ue_coords: np.ndarray,
    snr_th: float = SNR_THRESHOLD_DB,
    w1: float = WEIGHT_COVERAGE,
    w2: float = WEIGHT_ENERGY,
    w3: float = WEIGHT_INTERFERENCE,
) -> ObjectiveValues:
    """Đánh giá toàn diện một nghiệm vị trí UAV."""
    # 1. Tính toán vật lý kênh truyền
    distances = compute_distance_3d(uav_coords, ue_coords)
    angles_deg = compute_elevation_angle_deg(uav_coords, ue_coords, distances)
    p_los = compute_los_probability(angles_deg)
    path_loss = compute_path_loss(distances, p_los)
    snr = compute_snr(path_loss)

    # 2. Tính các hàm mục tiêu f1, f2, f3
    f1, covered_mask = calculate_coverage_rate(snr, snr_th=snr_th)
    f2 = calculate_energy_consumption(uav_coords)
    f3 = calculate_interference_rate(snr, snr_th=snr_th)

    # 3. Hàm Fitness tổng hợp: Fitness = w1*f1 - w2*f2 - w3*f3
    fitness = w1 * f1 - w2 * f2 - w3 * f3

    total_m = ue_coords.shape[0]
    covered_count = int(np.sum(covered_mask))

    return ObjectiveValues(
        fitness=float(fitness),
        coverage_rate=f1,
        energy_normalized=f2,
        interference_rate=f3,
        covered_users_count=covered_count,
        total_users_count=total_m,
    )
