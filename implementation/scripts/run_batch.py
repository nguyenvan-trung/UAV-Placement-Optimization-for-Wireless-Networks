"""Chạy hàng loạt (Batch Runner) các thuật toán trên nhiều bộ dữ liệu (Hỗ trợ Đa tiến trình - Multiprocessing)."""

import argparse
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

IMPLEMENTATION_DIR = Path(__file__).resolve().parents[1]
if str(IMPLEMENTATION_DIR) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_DIR))

# Thiết lập UTF-8 để tương thích console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

from src.algorithms import (
    GAOptimizer,
    GAParameters,
    HybridPSOGAOptimizer,
    HPSOGAParameters,
    HybridWOAPSOOptimizer,
    HWOAPSOParameters,
    IWOAOptimizer,
    IWOAParameters,
    PSOOptimizer,
    PSOParameters,
    WOAOptimizer,
    WOAParameters,
)
from src.constants.network import DEFAULT_NUM_UAVS
from src.constants.paths import DATASET_STORES_DIR, RESULTS_DIR
from src.input.data_loader import load_users
from src.input.data_validator import validate_users
from src.preprocessing.preprocessor import preprocess_users
from src.problem.objective import UAVPlacementProblem
from src.problem.solution_encoding import decode_uav_positions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chạy hàng loạt trên nhiều file CSV trong data/stores.")
    parser.add_argument(
        "--mode",
        choices=("representative", "all", "custom"),
        default="all",
        help="Chế độ: 'representative' (10 file 50->500), 'all' (toàn bộ 500 file), 'custom'.",
    )
    parser.add_argument("--uavs", type=int, default=DEFAULT_NUM_UAVS, help="Số lượng UAV.")
    parser.add_argument(
        "--random-uavs",
        action="store_true",
        help="Chọn ngẫu nhiên số UAV riêng cho từng dataset, cố định theo seed.",
    )
    parser.add_argument("--min-uavs", type=int, default=2, help="Số UAV tối thiểu khi bật --random-uavs.")
    parser.add_argument("--max-uavs", type=int, default=8, help="Số UAV tối đa khi bật --random-uavs.")
    parser.add_argument("--pop-size", type=int, default=25, help="Kích thước quần thể.")
    parser.add_argument("--iterations", type=int, default=35, help="Số vòng lặp.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=["GA", "PSO", "WOA", "H-PSO-GA", "H-WOA-PSO", "I-WOA"],
        choices=("GA", "PSO", "WOA", "H-PSO-GA", "H-WOA-PSO", "I-WOA"),
        help="Danh sách thuật toán cần chạy.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn tối đa số file CSV chạy.")
    parser.add_argument("--workers", type=int, default=min(12, os.cpu_count() or 4), help="Số luồng CPU xử lý song song.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=RESULTS_DIR,
        help="Thư mục lưu CSV, bảng tổng hợp và biểu đồ.",
    )
    return parser.parse_args()


def select_datasets(mode: str, limit: int | None = None) -> list[Path]:
    all_files = sorted(DATASET_STORES_DIR.glob("*_users_connect.csv"))
    if not all_files:
        print(f"Lỗi: Không tìm thấy file CSV nào trong {DATASET_STORES_DIR}")
        sys.exit(1)

    if mode == "all":
        selected = all_files
    elif mode == "representative":
        selected = all_files[:10]
    else:
        selected = all_files[:limit] if limit else all_files[:5]

    if limit is not None:
        selected = selected[:limit]

    return selected


def process_single_dataset(task_args: tuple) -> list[dict]:
    """Hàm xử lý độc lập từng file dataset trong process worker."""
    fpath_str, uavs, pop_size, iterations, seed, algorithms = task_args
    fpath = Path(fpath_str)

    df = load_users(fpath)
    validate_users(df)
    df = preprocess_users(df)
    ue_coords = df[["x_m", "y_m", "z_m"]].to_numpy()
    total_users = len(ue_coords)

    problem = UAVPlacementProblem(ue_coords=ue_coords, num_uavs=uavs)

    algo_factories = {
        "GA": lambda: GAOptimizer(GAParameters(population_size=pop_size, generations=iterations), seed=seed),
        "PSO": lambda: PSOOptimizer(PSOParameters(swarm_size=pop_size, iterations=iterations), seed=seed),
        "WOA": lambda: WOAOptimizer(WOAParameters(population_size=pop_size, iterations=iterations), seed=seed),
        "H-PSO-GA": lambda: HybridPSOGAOptimizer(HPSOGAParameters(population_size=pop_size, iterations=iterations), seed=seed),
        "H-WOA-PSO": lambda: HybridWOAPSOOptimizer(HWOAPSOParameters(population_size=pop_size, iterations=iterations), seed=seed),
        "I-WOA": lambda: IWOAOptimizer(IWOAParameters(population_size=pop_size, iterations=iterations), seed=seed),
    }

    records = []
    for algo_name in algorithms:
        if algo_name not in algo_factories:
            continue
        opt = algo_factories[algo_name]()
        res = opt.optimize(problem)
        m = problem.evaluate_detailed(res.best_position)

        records.append({
            "Dataset": fpath.name,
            "Total_Users": total_users,
            "Num_UAVs": uavs,
            "Algorithm": algo_name,
            "Population_Size": pop_size,
            "Iterations": iterations,
            "Seed": seed,
            "Fitness": res.best_objective,
            "Coverage_Rate": m.coverage_rate,
            "Covered_Users": m.covered_users_count,
            "Energy_Normalized": m.energy_normalized,
            "Interference_Rate": m.interference_rate,
            "Runtime_Seconds": res.runtime_seconds,
        })

    return records


def main() -> None:
    args = parse_args()
    if args.uavs <= 0:
        raise ValueError("--uavs phải lớn hơn 0.")
    if args.min_uavs <= 0 or args.max_uavs < args.min_uavs:
        raise ValueError("--min-uavs và --max-uavs phải thỏa 0 < min <= max.")
    if args.pop_size <= 0 or args.iterations <= 0:
        raise ValueError("--pop-size và --iterations phải lớn hơn 0.")
    if args.workers <= 0:
        raise ValueError("--workers phải lớn hơn 0.")

    files = select_datasets(args.mode, args.limit)
    if args.random_uavs:
        uav_rng = np.random.default_rng(args.seed)
        uavs_per_dataset = uav_rng.integers(
            args.min_uavs,
            args.max_uavs + 1,
            size=len(files),
        ).tolist()
    else:
        uavs_per_dataset = [args.uavs] * len(files)

    print("=" * 85)
    print("CHẠY HÀNG LOẠT (BATCH RUNNER) TRÊN TOÀN BỘ BỘ DỮ LIỆU UAV")
    print(f"Chế độ        : {args.mode}")
    print(f"Số lượng file : {len(files)} files")
    print(f"Thuật toán    : {args.algorithms}")
    print(f"Số luồng CPU  : {args.workers} workers song song")
    uav_description = (
        f"random {args.min_uavs}-{args.max_uavs} (seed {args.seed})"
        if args.random_uavs
        else str(args.uavs)
    )
    print(f"Cấu hình      : UAVs={uav_description} | PopSize={args.pop_size} | Iterations={args.iterations} | Seed={args.seed}")
    print("=" * 85)

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    out_csv = output_dir / ("batch_results_all_500_datasets.csv" if args.mode == "all" else f"batch_results_{args.mode}.csv")

    records = []
    failures: list[str] = []
    task_list = [
        (str(fpath), uavs, args.pop_size, args.iterations, args.seed, args.algorithms)
        for fpath, uavs in zip(files, uavs_per_dataset)
    ]

    start_time = time.time()
    completed_count = 0

    if args.workers > 1 and len(files) > 1:
        print(f"\n🚀 Đang khởi chạy {args.workers} tiến trình xử lý song song...")
        with ProcessPoolExecutor(max_workers=args.workers) as executor:
            future_to_file = {
                executor.submit(process_single_dataset, task): task[0]
                for task in task_list
            }

            for future in as_completed(future_to_file):
                fpath_str = future_to_file[future]
                completed_count += 1
                try:
                    file_records = future.result()
                    records.extend(file_records)
                    
                    # Log tiến độ ngắn gọn
                    if completed_count % 10 == 0 or completed_count == len(files):
                        elapsed = time.time() - start_time
                        speed = completed_count / elapsed if elapsed > 0 else 0
                        print(f"[{completed_count:3d}/{len(files):3d}] ({completed_count*100/len(files):5.1f}%) | {Path(fpath_str).name} | Tốc độ: {speed:.1f} files/s | Thời gian: {elapsed:.0f}s")
                    
                    # Lưu định kỳ mỗi 25 files đề phòng sự cố
                    if completed_count % 25 == 0:
                        temp_df = pd.DataFrame(records)
                        temp_df.to_csv(out_csv, index=False)

                except Exception as e:
                    print(f"❌ Lỗi khi xử lý file {Path(fpath_str).name}: {e}")
                    failures.append(f"{Path(fpath_str).name}: {e}")

    else:
        # Chạy tuần tự nếu workers=1
        for idx, task in enumerate(task_list, 1):
            fpath_name = Path(task[0]).name
            print(f"[{idx}/{len(files)}] Đang xử lý: {fpath_name}")
            file_records = process_single_dataset(task)
            records.extend(file_records)
            pd.DataFrame(records).to_csv(out_csv, index=False)

    total_df = pd.DataFrame(records)
    total_df.to_csv(out_csv, index=False)

    expected_rows = len(files) * len(args.algorithms)
    if failures or len(total_df) != expected_rows:
        details = "; ".join(failures[:10]) if failures else "số dòng kết quả không khớp cấu hình"
        raise RuntimeError(
            f"Batch chưa đầy đủ: có {len(total_df)}/{expected_rows} kết quả. {details}"
        )

    total_elapsed = time.time() - start_time
    print("\n" + "=" * 85)
    print(f"🎉 HOÀN TẤT TOÀN BỘ {len(files)} FILES BỘ DỮ LIỆU! (Thời gian: {total_elapsed:.1f}s)")
    print(f"-> Đã lưu tại: {out_csv}")
    print("=" * 85)

    print("\n📊 Đang tự động kết xuất bảng tổng hợp và bộ biểu đồ demo...")
    generate_summary_reports_and_plots(out_csv, iterations=args.iterations, seed=args.seed)
    print(f"✅ Hoàn tất kết xuất bảng báo cáo và biểu đồ trong {output_dir}")


def generate_summary_reports_and_plots(
    csv_path: Path,
    iterations: int = 35,
    seed: int = 42,
) -> None:
    if not csv_path.exists():
        return
    df = pd.read_csv(csv_path)
    results_dir = csv_path.parent

    # 1. Bảng tổng hợp theo Total_Users và Algorithm
    agg_df = df.groupby(["Total_Users", "Algorithm"]).agg({
        "Fitness": ["mean", "std", "max", "min"],
        "Coverage_Rate": "mean",
        "Energy_Normalized": "mean",
        "Interference_Rate": "mean",
        "Runtime_Seconds": "mean",
    }).reset_index()
    agg_df.columns = ["User_Count", "Algorithm", "Fitness", "Fitness_Std", "Fitness_Max", "Fitness_Min", "Coverage_Rate", "Energy_Normalized", "Interference_Rate", "Runtime_Seconds"]

    scalability_csv = results_dir / "scalability_summary_50_to_500.csv"
    agg_df.to_csv(scalability_csv, index=False)

    # 2. Tổng hợp thêm theo số UAV để không gộp lẫn các cấu hình khác nhau.
    uav_summary = df.groupby(["Num_UAVs", "Algorithm"]).agg({
        "Fitness": ["mean", "std", "max", "min"],
        "Coverage_Rate": "mean",
        "Energy_Normalized": "mean",
        "Interference_Rate": "mean",
        "Runtime_Seconds": "mean",
    }).reset_index()
    uav_summary.columns = [
        "Num_UAVs", "Algorithm", "Fitness", "Fitness_Std", "Fitness_Max",
        "Fitness_Min", "Coverage_Rate", "Energy_Normalized",
        "Interference_Rate", "Runtime_Seconds",
    ]
    uav_summary.to_csv(results_dir / "uav_count_summary.csv", index=False)
    uav_dataset_counts = df[["Dataset", "Num_UAVs"]].drop_duplicates()
    uav_distribution = (
        uav_dataset_counts.groupby("Num_UAVs")
        .size()
        .reindex(
            range(
                int(uav_dataset_counts["Num_UAVs"].min()),
                int(uav_dataset_counts["Num_UAVs"].max()) + 1,
            ),
            fill_value=0,
        )
        .rename("Dataset_Count")
        .rename_axis("Num_UAVs")
        .reset_index()
    )
    uav_distribution.to_csv(
        results_dir / "uav_count_distribution.csv",
        index=False,
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(
        uav_distribution["Num_UAVs"],
        uav_distribution["Dataset_Count"],
        color="#2b5c8f",
    )
    ax.bar_label(bars)
    ax.set_title("Phân bố số UAV được chọn ngẫu nhiên theo dataset")
    ax.set_xlabel("Số UAV")
    ax.set_ylabel("Số dataset")
    ax.set_xticks(uav_distribution["Num_UAVs"])
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    fig.tight_layout()
    fig.savefig(results_dir / "uav_count_distribution.png", dpi=300)
    plt.close(fig)

    # 3. Vẽ bộ 4 biểu đồ đa tiêu chí
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    plt.rcParams.update({"font.size": 11, "font.family": "sans-serif"})

    algorithms = ["GA", "PSO", "WOA", "H-PSO-GA", "H-WOA-PSO", "I-WOA"]
    markers = {"GA": "o", "PSO": "s", "WOA": "^", "H-PSO-GA": "D", "H-WOA-PSO": "v", "I-WOA": "*"}
    colors = {
        "GA": "#1f77b4", "PSO": "#ff7f0e", "WOA": "#2ca02c",
        "H-PSO-GA": "#9467bd", "H-WOA-PSO": "#8c564b", "I-WOA": "#d62728"
    }
    linewidths = {"GA": 1.8, "PSO": 1.8, "WOA": 1.8, "H-PSO-GA": 2.0, "H-WOA-PSO": 2.0, "I-WOA": 3.2}

    # Fitness
    ax1 = axes[0, 0]
    for algo in algorithms:
        sub = agg_df[agg_df["Algorithm"] == algo].sort_values("User_Count")
        ax1.plot(sub["User_Count"], sub["Fitness"], label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo], markersize=8)
    ax1.set_title("Hàm Thích Nghi Tổng Hợp (Fitness) theo Quy Mô Người Dùng", fontweight="bold", fontsize=13)
    ax1.set_xlabel("Số lượng người dùng mặt đất (UEs)", fontweight="semibold")
    ax1.set_ylabel("Fitness (Càng cao càng tốt)", fontweight="semibold")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend(loc="lower left", framealpha=0.9)

    # Nhiễu
    ax2 = axes[0, 1]
    for algo in algorithms:
        sub = agg_df[agg_df["Algorithm"] == algo].sort_values("User_Count")
        ax2.plot(sub["User_Count"], sub["Interference_Rate"] * 100, label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo], markersize=8)
    ax2.set_title("Tỷ Lệ Nhiễu Giao Thoa f3 (%) theo Quy Mô", fontweight="bold", fontsize=13)
    ax2.set_xlabel("Số lượng người dùng mặt đất (UEs)", fontweight="semibold")
    ax2.set_ylabel("Nhiễu giao thoa f3 (%) (Càng thấp càng tốt)", fontweight="semibold")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend(loc="upper left", framealpha=0.9)

    # Phủ sóng
    ax3 = axes[1, 0]
    for algo in algorithms:
        sub = agg_df[agg_df["Algorithm"] == algo].sort_values("User_Count")
        ax3.plot(sub["User_Count"], sub["Coverage_Rate"] * 100, label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo], markersize=8)
    ax3.set_title("Tỷ Lệ Phủ Sóng f1 (%) theo Quy Mô Người Dùng", fontweight="bold", fontsize=13)
    ax3.set_xlabel("Số lượng người dùng mặt đất (UEs)", fontweight="semibold")
    ax3.set_ylabel("Tỷ lệ phủ sóng f1 (%)", fontweight="semibold")
    ax3.set_ylim([97.5, 100.5])
    ax3.grid(True, linestyle="--", alpha=0.6)
    ax3.legend(loc="lower left", framealpha=0.9)

    # Năng lượng
    ax4 = axes[1, 1]
    for algo in algorithms:
        sub = agg_df[agg_df["Algorithm"] == algo].sort_values("User_Count")
        ax4.plot(sub["User_Count"], sub["Energy_Normalized"], label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo], markersize=8)
    ax4.set_title("Mức Tiêu Thụ Năng Lượng Chuẩn Hóa f2 theo Quy Mô", fontweight="bold", fontsize=13)
    ax4.set_xlabel("Số lượng người dùng mặt đất (UEs)", fontweight="semibold")
    ax4.set_ylabel("Năng lượng f2 (Càng thấp càng tốt)", fontweight="semibold")
    ax4.grid(True, linestyle="--", alpha=0.6)
    ax4.legend(loc="upper left", framealpha=0.9)

    plt.tight_layout()
    scalability_plot_path = results_dir / "scalability_analysis_50_to_500.png"
    plt.savefig(scalability_plot_path, dpi=300)
    plt.close()

    # 3. Mô phỏng 3D UAV placement
    sample_rows = df[df["Total_Users"] == 200]
    sample_dataset = (
        DATASET_STORES_DIR / sample_rows.iloc[0]["Dataset"]
        if not sample_rows.empty
        else None
    )
    if sample_dataset is not None and sample_dataset.exists():
        raw_df = load_users(sample_dataset)
        validate_users(raw_df)
        clean_df = preprocess_users(raw_df)
        ue_coords = clean_df[["x_m", "y_m", "z_m"]].to_numpy()
        sample_uavs = int(sample_rows.iloc[0]["Num_UAVs"])
        problem = UAVPlacementProblem(ue_coords=ue_coords, num_uavs=sample_uavs)
        opt = IWOAOptimizer(
            IWOAParameters(population_size=25, iterations=iterations),
            seed=seed,
        )
        res = opt.optimize(problem)
        uav_coords = decode_uav_positions(problem.search_space.clip(res.best_position))

        fig = plt.figure(figsize=(12, 9))
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(ue_coords[:, 0], ue_coords[:, 1], ue_coords[:, 2], c="#2b5c8f", marker=".", alpha=0.6, s=35, label="Người dùng (UEs)")
        uav_colors = plt.cm.tab10(np.linspace(0, 1, sample_uavs))
        for i, (ux, uy, uz) in enumerate(uav_coords):
            ax.scatter(ux, uy, uz, c=uav_colors[i], marker="^", s=220, edgecolors="black", linewidths=1.5, label=f"UAV {i+1} (z={uz:.1f}m)")
            ax.plot([ux, ux], [uy, uy], [0, uz], color=uav_colors[i], linestyle="--", linewidth=1.5, alpha=0.8)
            theta = np.linspace(0, 2*np.pi, 100)
            radius = uz * np.tan(np.radians(45))
            cx = ux + radius * np.cos(theta)
            cy = uy + radius * np.sin(theta)
            cz = np.zeros_like(cx)
            ax.plot(cx, cy, cz, color=uav_colors[i], alpha=0.5, linewidth=1.2)

        ax.set_title(f"Mô phỏng vị trí {sample_uavs} UAVs và 200 UEs (I-WOA, {iterations} vòng lặp)", fontweight="bold", fontsize=14, pad=20)
        ax.set_xlabel("Tọa độ X (m)", fontweight="semibold")
        ax.set_ylabel("Tọa độ Y (m)", fontweight="semibold")
        ax.set_zlabel("Độ cao Z (m)", fontweight="semibold")
        ax.set_xlim([0, 1000])
        ax.set_ylim([0, 1000])
        ax.set_zlim([0, 300])
        ax.view_init(elev=28, azim=45)
        ax.legend(loc="upper right", framealpha=0.9)
        plt.tight_layout()
        plt.savefig(results_dir / "uav_3d_placement_demo.png", dpi=300)
        plt.close()

    # 4. Xuất DEMO_REPORT.md
    report_md_path = results_dir / "batch_results_all_500_datasets_report.md"
    pivot_fitness = agg_df.pivot(index="User_Count", columns="Algorithm", values="Fitness")
    pivot_interf = agg_df.pivot(index="User_Count", columns="Algorithm", values="Interference_Rate") * 100
    pivot_cov = agg_df.pivot(index="User_Count", columns="Algorithm", values="Coverage_Rate") * 100

    report_lines = [
        "# KẾT QUẢ BATCH TỐI ƯU VỊ TRÍ UAV 3D",
        "",
        f"- Số dataset: {df['Dataset'].nunique()}",
        f"- Số lượt tối ưu hóa: {len(df)}",
        f"- Số vòng lặp: {iterations}",
        f"- Seed: {seed}",
        f"- Số UAV được dùng: {', '.join(map(str, sorted(df['Num_UAVs'].unique())))}",
        "- Bảng fitness theo số user là trung bình trên các bộ dữ liệu có cùng số user; "
        "với số UAV ngẫu nhiên, hãy dùng thêm bảng `uav_count_summary.csv` để xem theo số UAV.",
        "- Chi tiết số UAV theo dataset: `uav_count_distribution.csv`",
        "## 1. Bảng So Sánh Fitness (Hàm Thích Nghi Tổng Hợp - Càng Cao Càng Tốt)",
        "",
        pivot_fitness.to_markdown(),
        "",
        "## 2. Bảng Tỷ Lệ Nhiễu Giao Thoa f3 (%) (Càng Thấp Càng Tốt)",
        "",
        pivot_interf.to_markdown(),
        "",
        "## 3. Bảng Tỷ Lệ Phủ Sóng f1 (%)",
        "",
        pivot_cov.to_markdown(),
        "",
        "## 4. Tóm Tắt Trung Bình Toàn Bộ 10 Quy Mô (50 -> 500 UEs)",
        "",
    ]
    mean_table = agg_df.groupby("Algorithm").agg({
        "Fitness": ["mean", "max"],
        "Coverage_Rate": "mean",
        "Energy_Normalized": "mean",
        "Interference_Rate": "mean",
        "Runtime_Seconds": "mean"
    })
    mean_table.columns = ["Fitness_TB", "Fitness_Max", "Coverage_TB", "Energy_TB", "Interf_TB", "Runtime_TB"]
    mean_table["Coverage_TB"] = (mean_table["Coverage_TB"] * 100).round(2).astype(str) + "%"
    mean_table["Interf_TB"] = (mean_table["Interf_TB"] * 100).round(2).astype(str) + "%"
    mean_table["Fitness_TB"] = mean_table["Fitness_TB"].round(4)
    mean_table["Fitness_Max"] = mean_table["Fitness_Max"].round(4)
    mean_table["Energy_TB"] = mean_table["Energy_TB"].round(4)
    mean_table["Runtime_TB"] = mean_table["Runtime_TB"].round(2).astype(str) + "s"

    report_lines.append(mean_table.to_markdown())
    report_lines.append("")

    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))


if __name__ == "__main__":
    main()
