"""Làm sạch và chuẩn hóa dữ liệu sau khi xác thực."""

import pandas as pd


def preprocess_users(data: pd.DataFrame) -> pd.DataFrame:
    return data.drop_duplicates(subset="user_id").dropna().reset_index(drop=True)
