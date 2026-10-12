"""Tạo bộ dataset chính thức và ảnh quan sát.

Chạy file này trước khi chạy thuật toán:

    python scripts/generate_dataset.py

CSV được lưu trong ``data/stores/`` và ảnh trong ``data/views/`` ở cấp gốc
dự án.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.constants.paths import DATASET_STORES_DIR, DATASET_VIEWS_DIR
from src.data_generation.synthetic_generator import (
    DEFAULT_DATASET_COUNT,
    DEFAULT_USER_COUNTS,
    build_dataset_counts,
    generate_dataset_suite,
)
from src.visualization.dataset_views import save_suite_views


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic UAV datasets")
    parser.add_argument(
        "--counts",
        nargs="+",
        type=int,
        default=None,
        help="Các kích thước user để lặp lại, mặc định: 50 100 ... 500",
    )
    parser.add_argument(
        "--num-datasets",
        type=int,
        default=DEFAULT_DATASET_COUNT,
        help=f"Số CSV cần tạo, mặc định: {DEFAULT_DATASET_COUNT}",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    user_counts = tuple(args.counts or DEFAULT_USER_COUNTS)
    counts = build_dataset_counts(
        dataset_count=args.num_datasets,
        user_counts=user_counts,
    )
    dataset_paths = generate_dataset_suite(
        output_dir=DATASET_STORES_DIR,
        counts=counts,
    )
    view_paths = save_suite_views(dataset_paths, DATASET_VIEWS_DIR)

    print(f"Da tao {len(dataset_paths)} dataset:")
    for path in dataset_paths:
        print(f"- {path}")
    print(f"Da tao {len(view_paths)} anh quan sat trong {DATASET_VIEWS_DIR}")


if __name__ == "__main__":
    main()
