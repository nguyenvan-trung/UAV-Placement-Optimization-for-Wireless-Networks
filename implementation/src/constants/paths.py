"""Đường dẫn cố định của dự án."""

from pathlib import Path

IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = IMPLEMENTATION_ROOT / "datasets"
RAW_DATA_DIR = DATASET_DIR / "raw"
PROCESSED_DATA_DIR = DATASET_DIR / "processed"
RESULTS_DIR = IMPLEMENTATION_ROOT / "results"
