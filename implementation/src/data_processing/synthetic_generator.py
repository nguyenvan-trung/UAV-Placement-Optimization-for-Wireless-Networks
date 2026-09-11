"""Tạo dataset giả để kiểm thử trước khi có dữ liệu thật."""

import numpy as np
import pandas as pd


def generate_users(count: int, width: float, height: float, seed: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "user_id": np.arange(count),
        "x": rng.uniform(0, width, count),
        "y": rng.uniform(0, height, count),
        "demand": np.ones(count),
    })
