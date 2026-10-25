"""Làm sạch dữ liệu sau khi xác thực."""

import pandas as pd


def preprocess_users(data: pd.DataFrame) -> pd.DataFrame:
    """Bỏ user trùng theo user_id, giữ DataFrame độc lập."""
    return data.drop_duplicates(subset="user_id").reset_index(drop=True)
