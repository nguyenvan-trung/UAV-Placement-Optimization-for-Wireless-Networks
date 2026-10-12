import warnings
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning)
from sklearn.cluster import KMeans

from ..constants.network import DEFAULT_MIN_ALTITUDE_M


def compute_kmeans_centroids(
    ue_coords: np.ndarray,
    num_uavs: int,
    random_state: int = 42,
) -> np.ndarray:
    """Chạy K-Means trên tọa độ 2D của UEs để tìm num_uavs tâm cụm.

    Parameters
    ----------
    ue_coords : np.ndarray, shape (M, 3) hoặc (M, 2)
        Tọa độ người dùng mặt đất.
    num_uavs : int
        Số lượng UAV cần đặt (số cụm k).
    random_state : int

    Returns
    -------
    np.ndarray, shape (num_uavs, 2)
        Tọa độ tâm cụm [x_c, y_c].
    """
    xy_coords = ue_coords[:, :2]
    kmeans = KMeans(n_clusters=num_uavs, random_state=random_state, n_init=10)
    kmeans.fit(xy_coords)
    return kmeans.cluster_centers_


def generate_kmeans_uav_initial_guess(
    ue_coords: np.ndarray,
    num_uavs: int,
    default_altitude: float = DEFAULT_MIN_ALTITUDE_M + 50.0,
    random_state: int = 42,
) -> np.ndarray:
    """Tạo vector nghiệm 1D gợi ý ban đầu dựa trên tâm cụm K-Means.

    Returns
    -------
    np.ndarray, shape (num_uavs * 3,)
        [x1, y1, z1, ..., xN, yN, zN]
    """
    centroids_2d = compute_kmeans_centroids(ue_coords, num_uavs, random_state=random_state)
    uav_positions = np.zeros((num_uavs, 3), dtype=float)
    uav_positions[:, :2] = centroids_2d
    uav_positions[:, 2] = default_altitude
    return uav_positions.ravel()
