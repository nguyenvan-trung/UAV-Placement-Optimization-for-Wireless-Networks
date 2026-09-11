"""Mô hình một UAV."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UAV:
    x: float
    y: float
    altitude: float
