"""Mô hình một người dùng mặt đất."""

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    user_id: int
    x: float
    y: float
    z: float = 0.0
    demand: float = 1.0
