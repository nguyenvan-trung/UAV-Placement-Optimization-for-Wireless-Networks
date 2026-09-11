"""Định dạng và lưu bảng so sánh."""

from pathlib import Path

import pandas as pd


def save_table(table: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path)
