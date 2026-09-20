"""Sinh dataset người dùng 3D theo các cụm dân cư và tòa nhà."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from src.constants.network import DEFAULT_AREA_HEIGHT_M, DEFAULT_AREA_WIDTH_M

DEFAULT_USER_COUNTS = (50, 100, 150, 200, 250, 300, 350, 400, 450, 500)
DEFAULT_DATASETS_PER_COUNT = 50
DEFAULT_DATASET_COUNT = len(DEFAULT_USER_COUNTS) * DEFAULT_DATASETS_PER_COUNT


def build_dataset_counts(
    dataset_count: int = DEFAULT_DATASET_COUNT,
    user_counts: tuple[int, ...] = DEFAULT_USER_COUNTS,
) -> tuple[int, ...]:
    """Tạo danh sách kích thước cho cả bộ dataset, lặp theo chu kỳ."""
    if dataset_count <= 0:
        raise ValueError("dataset_count phải lớn hơn 0")
    if not user_counts or any(count <= 0 for count in user_counts):
        raise ValueError("user_counts phải chứa các số lớn hơn 0")

    return tuple(user_counts[index % len(user_counts)] for index in range(dataset_count))


def generate_users(
    count: int,
    width: float = DEFAULT_AREA_WIDTH_M,
    height: float = DEFAULT_AREA_HEIGHT_M,
    seed: int = 42,
) -> pd.DataFrame:
    """Tạo điểm người dùng 3D theo hotspot, tòa nhà và nền rải thưa.

    Mỗi hotspot có một độ cao tòa nhà khác nhau. Phần lớn user thuộc các
    hotspot và được đặt ở các tầng; một phần nhỏ ở mặt đất/nền. Seed cố định
    giúp tái tạo đúng cùng một bộ dữ liệu.
    """
    if count <= 0:
        raise ValueError("count phải lớn hơn 0")
    if width <= 0 or height <= 0:
        raise ValueError("width và height phải lớn hơn 0")

    rng = np.random.default_rng(seed)
    cluster_count = int(rng.integers(3, 7))
    centers = rng.uniform(
        low=[0.12 * width, 0.12 * height],
        high=[0.88 * width, 0.88 * height],
        size=(cluster_count, 2),
    )
    clustered_count = int(round(count * 0.78))
    cluster_ids = rng.integers(0, cluster_count, size=clustered_count)
    spread = min(width, height) * 0.075
    clustered = centers[cluster_ids] + rng.normal(
        0.0, spread, size=(clustered_count, 2)
    )
    background = rng.uniform(
        low=[0.0, 0.0],
        high=[width, height],
        size=(count - clustered_count, 2),
    )
    coordinates = np.vstack((clustered, background))
    rng.shuffle(coordinates, axis=0)
    x = np.clip(coordinates[:, 0], 0.0, width)
    y = np.clip(coordinates[:, 1], 0.0, height)
    building_heights = rng.choice(
        np.array([0.0, 12.0, 24.0, 36.0, 60.0, 90.0, 120.0]),
        size=cluster_count,
        p=[0.12, 0.18, 0.22, 0.20, 0.14, 0.09, 0.05],
    )
    z_clustered = np.maximum(
        0.0,
        building_heights[cluster_ids]
        + rng.normal(0.0, 3.0, size=clustered_count),
    )
    z_clustered[building_heights[cluster_ids] == 0.0] = 0.0
    z_background = rng.choice(
        np.array([0.0, 6.0, 12.0, 18.0, 24.0]),
        size=count - clustered_count,
        p=[0.35, 0.25, 0.20, 0.12, 0.08],
    )
    z = np.concatenate((z_clustered, z_background))
    rng.shuffle(z)
    user_id = np.arange(1, count + 1, dtype=int)
    demand = 1.0 + 0.25 * ((user_id - 1) % 5)

    return pd.DataFrame(
        {
            "user_id": user_id,
            "x_m": np.round(x, 3),
            "y_m": np.round(y, 3),
            "z_m": np.round(z, 3),
            "demand": np.round(demand, 3),
        }
    )


def save_synthetic_dataset(dataset: pd.DataFrame, output_path: str | Path) -> Path:
    """Lưu dataset vào CSV."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(path, index=False)
    return path


def generate_dataset_suite(
    output_dir: str | Path,
    counts: tuple[int, ...] | None = None,
    width: float = DEFAULT_AREA_WIDTH_M,
    height: float = DEFAULT_AREA_HEIGHT_M,
    seed: int = 42,
) -> list[Path]:
    """Sinh bộ file theo thứ tự tên.

    Khi không truyền ``counts``, tạo mặc định 500 dataset: mỗi kích thước
    từ 50 đến 500 users có 50 bộ.
    """
    output_dir = Path(output_dir)
    counts = counts or build_dataset_counts()
    saved_paths: list[Path] = []
    for serial, count in enumerate(counts, start=1):
        dataset = generate_users(
            count,
            width=width,
            height=height,
            seed=seed + serial - 1,
        )
        file_name = f"{serial:03d}_UAV_3D_{count}_users_connect.csv"
        saved_paths.append(save_synthetic_dataset(dataset, output_dir / file_name))
    return saved_paths


if __name__ == "__main__":
    for path in generate_dataset_suite():
        print(path)
