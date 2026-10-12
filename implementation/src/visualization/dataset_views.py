"""Tạo các ảnh quan sát dataset từ nhiều hướng."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_dataset_views(
    dataset_path: str | Path,
    output_dir: str | Path,
    width: float = 1000.0,
    height: float = 1000.0,
) -> list[Path]:
    """Xuất top, front, side và phối cảnh 3D cho một file CSV."""
    dataset_path = Path(dataset_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(dataset_path)
    stem = dataset_path.stem
    views: list[tuple[str, str]] = [
        ("top", "Nhìn từ trên xuống (X-Y)"),
        ("front", "Mặt đứng (X-Z)"),
        ("side", "Mặt bên (Y-Z)"),
    ]
    saved: list[Path] = []

    for suffix, title in views:
        fig, ax = plt.subplots(figsize=(8, 7))
        if suffix == "top":
            ax.scatter(data["x_m"], data["y_m"], c=data["demand"], cmap="viridis", s=16)
            ax.set(xlabel="X (m)", ylabel="Y (m)")
        elif suffix == "front":
            ax.scatter(data["x_m"], data["z_m"], c=data["demand"], cmap="viridis", s=16)
            ax.set(xlabel="X (m)", ylabel="Z (m)")
        else:
            ax.scatter(data["y_m"], data["z_m"], c=data["demand"], cmap="viridis", s=16)
            ax.set(xlabel="Y (m)", ylabel="Z (m)")
        ax.set_title(f"{stem} - {title}")
        if suffix == "top":
            ax.set_aspect("equal")
        ax.grid(True, alpha=0.25)
        figure_path = output_dir / f"{suffix}.png"
        fig.savefig(figure_path, dpi=160, bbox_inches="tight")
        plt.close(fig)
        saved.append(figure_path)

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(data["x_m"], data["y_m"], data["z_m"], c=data["demand"], cmap="viridis", s=16)
    ax.set(xlabel="X (m)", ylabel="Y (m)", zlabel="Z (m)")
    ax.set_title(f"{stem} - Phối cảnh 3D")
    figure_path = output_dir / "3d.png"
    fig.savefig(figure_path, dpi=160, bbox_inches="tight")
    plt.close(fig)
    saved.append(figure_path)
    return saved


def save_suite_views(dataset_paths: list[Path], output_dir: str | Path) -> list[Path]:
    """Tạo ảnh cho toàn bộ dataset, mỗi dataset có một thư mục riêng."""
    saved: list[Path] = []
    for dataset_path in dataset_paths:
        dataset_output_dir = Path(output_dir) / dataset_path.stem
        saved.extend(save_dataset_views(dataset_path, dataset_output_dir))
    return saved
