"""Kiểm tra schema và giá trị không hợp lệ của dữ liệu đầu vào."""

import pandas as pd

REQUIRED_USER_COLUMNS = {"user_id", "x", "y", "demand"}


def validate_users(data: pd.DataFrame) -> None:
    missing = REQUIRED_USER_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Thiếu các cột bắt buộc: {sorted(missing)}")
