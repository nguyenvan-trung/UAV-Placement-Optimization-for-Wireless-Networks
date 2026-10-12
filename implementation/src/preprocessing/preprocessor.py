"""Làm sạch dữ liệu sau khi xác thực."""

import pandas as pd


def preprocess_users(data: pd.DataFrame) -> pd.DataFrame:
    """Bỏ user trùng hoặc thiếu giá trị, giữ DataFrame độc lập."""
    return data.drop_duplicates(subset="user_id").dropna().reset_index(drop=True)
