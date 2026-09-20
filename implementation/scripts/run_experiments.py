"""Chạy nhiều seed, tổng hợp bảng và lưu biểu đồ thí nghiệm."""

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.constants.experiment import DEFAULT_SEEDS


def main() -> None:
    print(f"Seeds: {DEFAULT_SEEDS}")
    print("TODO: run GA/PSO/WOA and save outputs to results/.")


if __name__ == "__main__":
    main()
