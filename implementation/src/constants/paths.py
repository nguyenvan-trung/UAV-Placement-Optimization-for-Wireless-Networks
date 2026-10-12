"""Đường dẫn cố định của dự án."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
IMPLEMENTATION_ROOT = PROJECT_ROOT / "implementation"
DATASET_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATASET_DIR / "raw"
DATASET_STORES_DIR = DATASET_DIR / "stores"
DATASET_VIEWS_DIR = DATASET_DIR / "views"
RESULTS_DIR = IMPLEMENTATION_ROOT / "results"
