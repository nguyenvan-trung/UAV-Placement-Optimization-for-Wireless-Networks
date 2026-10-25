"""Kiểm tra schema và giá trị của dữ liệu người dùng đầu vào."""

import numpy as np
import pandas as pd

REQUIRED_USER_COLUMNS = {"user_id", "x_m", "y_m", "z_m", "demand"}
NUMERIC_USER_COLUMNS = ("x_m", "y_m", "z_m", "demand")


def validate_users(data: pd.DataFrame) -> None:
    """Báo lỗi rõ ràng nếu dữ liệu user sai schema hoặc chứa giá trị không hợp lệ."""
    missing = REQUIRED_USER_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"Thiếu các cột bắt buộc: {sorted(missing)}")

    if data.empty:
        raise ValueError("Dataset không chứa user nào.")

    required_columns = sorted(REQUIRED_USER_COLUMNS)
    null_columns = data[required_columns].columns[
        data[required_columns].isna().any()
    ].tolist()
    if null_columns:
        raise ValueError(f"Các cột bắt buộc không được chứa giá trị thiếu: {null_columns}")

    for column in NUMERIC_USER_COLUMNS:
        values = pd.to_numeric(data[column], errors="coerce")
        if values.isna().any() or not np.isfinite(values.to_numpy(dtype=float)).all():
            raise ValueError(f"Cột '{column}' phải chứa các giá trị số hữu hạn.")
