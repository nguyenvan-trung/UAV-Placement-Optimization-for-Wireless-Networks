"""Đọc dataset từ CSV và trả về DataFrame."""

from pathlib import Path

import pandas as pd


def load_users(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)
