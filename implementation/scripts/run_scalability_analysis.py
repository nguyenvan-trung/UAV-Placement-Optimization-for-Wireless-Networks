"""Thực nghiệm phân tích khả năng mở rộng (Scalability Analysis) theo quy mô người dùng.

So sánh GA, PSO, WOA, H-PSO-GA, H-WOA-PSO, và I-WOA trên các mức quy mô:
50, 100, 200, 300, 400, 500 users.
Xuất bảng tổng hợp CSV và biểu đồ đồ thị đa tiêu chí (Fitness, Interference, Coverage, Energy).
"""

import argparse
import sys
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phân tích hiệu năng theo quy mô người dùng.")
    parser.add_argument("--uavs", type=int, default=DEFAULT_NUM_UAVS, help="Số lượng UAV (mặc định: 4).")
    parser.add_argument("--pop-size", type=int, default=25, help="Kích thước quần thể.")
    parser.add_argument("--iterations", type=int, default=35, help="Số vòng lặp tối ưu.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Chọn các file đại diện cho các mức quy mô người dùng
    scale_files = [
        ("50", DATASET_STORES_DIR / "001_UAV_3D_50_users_connect.csv"),
        ("100", DATASET_STORES_DIR / "002_UAV_3D_100_users_connect.csv"),
        ("200", DATASET_STORES_DIR / "004_UAV_3D_200_users_connect.csv"),
        ("300", DATASET_STORES_DIR / "006_UAV_3D_300_users_connect.csv"),
        ("400", DATASET_STORES_DIR / "008_UAV_3D_400_users_connect.csv"),
        ("500", DATASET_STORES_DIR / "010_UAV_3D_500_users_connect.csv"),
    ]

    print("=" * 85)
    print("PHÂN TÍCH KHẢ NĂNG MỞ RỘNG (SCALABILITY ANALYSIS) 50 -> 500 USERS")
    print(f"Cấu hình: UAVs={args.uavs} | PopSize={args.pop_size} | Iterations={args.iterations} | Seed={args.seed}")
    print("=" * 85)

    records = []

    algo_factories = {
        "GA": lambda: GAOptimizer(GAParameters(population_size=args.pop_size, generations=args.iterations), seed=args.seed),
        "PSO": lambda: PSOOptimizer(PSOParameters(swarm_size=args.pop_size, iterations=args.iterations), seed=args.seed),
        "WOA": lambda: WOAOptimizer(WOAParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
        "H-PSO-GA": lambda: HybridPSOGAOptimizer(HPSOGAParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
        "H-WOA-PSO": lambda: HybridWOAPSOOptimizer(HWOAPSOParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
        "I-WOA": lambda: IWOAOptimizer(IWOAParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
    }

    for label, fpath in scale_files:
        if not fpath.exists():
            print(f"Bỏ qua file không tồn tại: {fpath.name}")
            continue

        df = load_users(fpath)
        validate_users(df)
        df = preprocess_users(df)
        ue_coords = df[["x_m", "y_m", "z_m"]].to_numpy()
        total_users = len(ue_coords)

        print(f"\n>>> Đang đánh giá mức quy mô: {total_users} người dùng ({fpath.name})")
        problem = UAVPlacementProblem(ue_coords=ue_coords, num_uavs=args.uavs)

        for algo_name, factory in algo_factories.items():
            opt = factory()
            res = opt.optimize(problem)
            m = problem.evaluate_detailed(res.best_position)

            records.append({
                "User_Count": total_users,
                "Algorithm": algo_name,
                "Fitness": res.best_objective,
                "Coverage_Rate": m.coverage_rate,
                "Energy_Normalized": m.energy_normalized,
                "Interference_Rate": m.interference_rate,
                "Runtime_Seconds": res.runtime_seconds,
            })
            print(f"   ► {algo_name:<11} | Fit: {res.best_objective:.4f} | Cov: {m.coverage_rate*100:>5.1f}% | Interf: {m.interference_rate*100:>5.1f}% | Time: {res.runtime_seconds:.2f}s")

    results_df = pd.DataFrame(records)

    # Lưu kết quả CSV
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / "scalability_summary_50_to_500.csv"
    results_df.to_csv(csv_path, index=False)
    print("\n" + "=" * 85)
    print(f"✅ Đã lưu dữ liệu tổng hợp tại: {csv_path}")

    # Vẽ bộ 4 biểu đồ phân tích chuyên sâu
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    plt.rcParams.update({"font.size": 11})

    user_counts = sorted(results_df["User_Count"].unique())
    algorithms = list(algo_factories.keys())
    markers = {"GA": "o", "PSO": "s", "WOA": "^", "H-PSO-GA": "D", "H-WOA-PSO": "v", "I-WOA": "*"}
    colors = {"GA": "#1f77b4", "PSO": "#ff7f0e", "WOA": "#2ca02c", "H-PSO-GA": "#9467bd", "H-WOA-PSO": "#8c564b", "I-WOA": "#d62728"}
    linewidths = {"GA": 1.8, "PSO": 1.8, "WOA": 1.8, "H-PSO-GA": 2.0, "H-WOA-PSO": 2.0, "I-WOA": 3.0}

    # 1. Biểu đồ Fitness
    ax1 = axes[0, 0]
    for algo in algorithms:
        sub = results_df[results_df["Algorithm"] == algo]
        ax1.plot(sub["User_Count"], sub["Fitness"], label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo])
    ax1.set_title("Hàm thích nghi tổng hợp (Fitness) theo số lượng người dùng", fontweight="bold")
    ax1.set_xlabel("Số lượng người dùng mặt đất (UEs)")
    ax1.set_ylabel("Fitness (Càng cao càng tốt)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    # 2. Biểu đồ Nhiễu giao thoa (Interference Rate - f3)
    ax2 = axes[0, 1]
    for algo in algorithms:
        sub = results_df[results_df["Algorithm"] == algo]
        ax2.plot(sub["User_Count"], sub["Interference_Rate"] * 100, label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo])
    ax2.set_title("Tỷ lệ nhiễu giao thoa chồng lấn (%) theo số lượng người dùng", fontweight="bold")
    ax2.set_xlabel("Số lượng người dùng mặt đất (UEs)")
    ax2.set_ylabel("Tỷ lệ nhiễu f3 (%) (Càng thấp càng tốt)")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    # 3. Biểu đồ Độ phủ sóng (Coverage Rate - f1)
    ax3 = axes[1, 0]
    for algo in algorithms:
        sub = results_df[results_df["Algorithm"] == algo]
        ax3.plot(sub["User_Count"], sub["Coverage_Rate"] * 100, label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo])
    ax3.set_title("Tỷ lệ phủ sóng (%) theo số lượng người dùng", fontweight="bold")
    ax3.set_xlabel("Số lượng người dùng mặt đất (UEs)")
    ax3.set_ylabel("Tỷ lệ phủ sóng f1 (%)")
    ax3.grid(True, linestyle="--", alpha=0.6)
    ax3.legend()

    # 4. Biểu đồ Năng lượng tiêu thụ (f2)
    ax4 = axes[1, 1]
    for algo in algorithms:
        sub = results_df[results_df["Algorithm"] == algo]
        ax4.plot(sub["User_Count"], sub["Energy_Normalized"], label=algo, marker=markers[algo], color=colors[algo], linewidth=linewidths[algo])
    ax4.set_title("Mức tiêu thụ năng lượng chuẩn hóa theo số lượng người dùng", fontweight="bold")
    ax4.set_xlabel("Số lượng người dùng mặt đất (UEs)")
    ax4.set_ylabel("Năng lượng f2 (Càng thấp càng tốt)")
    ax4.grid(True, linestyle="--", alpha=0.6)
    ax4.legend()

    plt.tight_layout()
    plot_path = RESULTS_DIR / "scalability_analysis_50_to_500.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"📈 Đã lưu bộ biểu đồ phân tích mở rộng tại: {plot_path}")
    print("=" * 85)


if __name__ == "__main__":
    main()
