"""Mô hình kênh truyền Air-to-Ground (A2G) 5G/6G."""

import numpy as np

from ..constants.network import (
    CARRIER_FREQUENCY_HZ,
    ENV_A,
    ENV_B,
    ETA_LOS,
    ETA_NLOS,
    NOISE_POWER_DBM,
    SPEED_OF_LIGHT,
    TRANSMIT_POWER_DBM,
)


def compute_distance_3d(uav_coords: np.ndarray, ue_coords: np.ndarray) -> np.ndarray:
    """Tính khoảng cách hình học 3D Euclidean giữa N UAVs và M UEs.

    Parameters
    ----------
    uav_coords : np.ndarray, shape (N, 3)
        Tọa độ [x, y, z] của các UAV.
    ue_coords : np.ndarray, shape (M, 3)
        Tọa độ [x, y, z] của người dùng mặt đất.

    Returns
    -------
    np.ndarray, shape (N, M)
        Ma trận khoảng cách d_ij (mét).
    """
    diff = uav_coords[:, np.newaxis, :] - ue_coords[np.newaxis, :, :]
    dist = np.sqrt(np.sum(diff**2, axis=-1))
    return np.maximum(dist, 1e-3)


def compute_elevation_angle_deg(
    uav_coords: np.ndarray, ue_coords: np.ndarray, distances: np.ndarray
) -> np.ndarray:
    """Tính góc ngẩng elevation angle theta_ij (độ).

    Parameters
    ----------
    uav_coords : np.ndarray, shape (N, 3)
    ue_coords : np.ndarray, shape (M, 3)
    distances : np.ndarray, shape (N, M)

    Returns
    -------
    np.ndarray, shape (N, M)
        Góc ngẩng tính bằng độ [0, 90].
    """
    delta_z = uav_coords[:, np.newaxis, 2] - ue_coords[np.newaxis, :, 2]
    sin_theta = np.clip(delta_z / distances, 0.0, 1.0)
    theta_rad = np.arcsin(sin_theta)
    return np.degrees(theta_rad)


def compute_los_probability(
    theta_deg: np.ndarray, a: float = ENV_A, b: float = ENV_B
) -> np.ndarray:
    """Tính xác suất nhìn thẳng (Probability of LoS) theo Al-Hourani.

    P_LoS(theta) = 1 / (1 + a * exp(-b * (theta - a)))
    """
    exponent = -b * (theta_deg - a)
    # Clip exponent để tránh tràn số float exp
    exponent = np.clip(exponent, -60.0, 60.0)
    return 1.0 / (1.0 + a * np.exp(exponent))


def compute_path_loss(
    distances: np.ndarray,
    p_los: np.ndarray,
    freq_hz: float = CARRIER_FREQUENCY_HZ,
    eta_los: float = ETA_LOS,
    eta_nlos: float = ETA_NLOS,
    c: float = SPEED_OF_LIGHT,
) -> np.ndarray:
    """Tính suy hao đường truyền tổng hợp (Pathloss) d_ij.

    PL_LoS = 20*log10(4*pi*f*d/c) + eta_LoS
    PL_NLoS = 20*log10(4*pi*f*d/c) + eta_NLoS
    PL = P_LoS * PL_LoS + (1 - P_LoS) * PL_NLoS
    """
    fspl = 20.0 * np.log10(distances) + 20.0 * np.log10(4.0 * np.pi * freq_hz / c)
    pl_los = fspl + eta_los
    pl_nlos = fspl + eta_nlos
    return p_los * pl_los + (1.0 - p_los) * pl_nlos


def compute_snr(
    path_loss: np.ndarray,
    p_tx_dbm: float = TRANSMIT_POWER_DBM,
    noise_dbm: float = NOISE_POWER_DBM,
) -> np.ndarray:
    """Tính SNR_ij = P_rx - Noise (dB)."""
    p_rx_dbm = p_tx_dbm - path_loss
    return p_rx_dbm - noise_dbm
