"""Kiểm tra schema và giá trị của dữ liệu người dùng đầu vào."""

import pandas as pd

REQUIRED_USER_COLUMNS = {"user_id", "x_m", "y_m", "z_m", "demand"}


def validate_users(data: pd.DataFrame) -> None:
    """Báo lỗi rõ ràng nếu CSV không đúng schema hiện tại."""
    missing = REQUIRED_USER_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Thiếu các cột bắt buộc: {sorted(missing)}")
