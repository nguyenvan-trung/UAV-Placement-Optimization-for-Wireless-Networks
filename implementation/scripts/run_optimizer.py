"""Điểm chạy và so sánh toàn diện các thuật toán tối ưu vị trí UAV 3D."""

import argparse
import sys
from pathlib import Path

# Thêm đường dẫn implementation vào sys.path để chạy từ bất kỳ thư mục nào
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

from src.algorithms import (
    GAParameters,
    GAOptimizer,
    HPSOGAParameters,
    HybridPSOGAOptimizer,
    HWOAPSOParameters,
    HybridWOAPSOOptimizer,
    IWOAParameters,
    IWOAOptimizer,
    PSOParameters,
    PSOOptimizer,
    WOAParameters,
    WOAOptimizer,
)
from src.constants.network import DEFAULT_NUM_UAVS
from src.constants.paths import RESULTS_DIR
from src.input.data_loader import load_users
from src.input.data_validator import validate_users
from src.preprocessing.preprocessor import preprocess_users
from src.problem.objective import UAVPlacementProblem


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chạy tối ưu hóa vị trí UAV 3D trong mạng không dây 5G/6G.")
    parser.add_argument(
        "--algorithm",
        choices=("GA", "PSO", "WOA", "H-PSO-GA", "H-WOA-PSO", "I-WOA", "all"),
        default="all",
        help="Thuật toán muốn chạy hoặc 'all' để so sánh tất cả.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed tái lập kết quả.")
    parser.add_argument("--dataset", type=str, required=True, help="Đường dẫn tới file CSV người dùng.")
    parser.add_argument("--uavs", type=int, default=DEFAULT_NUM_UAVS, help="Số lượng UAV (mặc định: 4).")
    parser.add_argument("--pop-size", type=int, default=30, help="Kích thước quần thể (mặc định: 30).")
    parser.add_argument("--iterations", type=int, default=50, help="Số thế hệ/vòng lặp tối đa (mặc định: 50).")
    parser.add_argument("--no-plot", action="store_true", help="Không lưu biểu đồ hội tụ.")
    return parser.parse_args()


def get_optimizers(args: argparse.Namespace) -> dict:
    all_opts = {
        "GA": GAOptimizer(
            GAParameters(population_size=args.pop_size, generations=args.iterations),
            seed=args.seed,
        ),
        "PSO": PSOOptimizer(
            PSOParameters(swarm_size=args.pop_size, iterations=args.iterations),
            seed=args.seed,
        ),
        "WOA": WOAOptimizer(
            WOAParameters(population_size=args.pop_size, iterations=args.iterations),
            seed=args.seed,
        ),
        "H-PSO-GA": HybridPSOGAOptimizer(
            HPSOGAParameters(population_size=args.pop_size, iterations=args.iterations),
            seed=args.seed,
        ),
        "H-WOA-PSO": HybridWOAPSOOptimizer(
            HWOAPSOParameters(population_size=args.pop_size, iterations=args.iterations),
            seed=args.seed,
        ),
        "I-WOA": IWOAOptimizer(
            IWOAParameters(population_size=args.pop_size, iterations=args.iterations),
            seed=args.seed,
        ),
    }

    if args.algorithm == "all":
        return all_opts
    return {args.algorithm: all_opts[args.algorithm]}


def main() -> None:
    args = parse_args()
    dataset_path = Path(args.dataset)
    if not dataset_path.is_absolute():
        dataset_path = (Path.cwd() / dataset_path).resolve()

    if not dataset_path.exists():
        print(f"Lỗi: Không tìm thấy file dữ liệu tại {dataset_path}")
        sys.exit(1)

    print("=" * 80)
    print("   UAV 3D PLACEMENT OPTIMIZATION FOR WIRELESS NETWORKS")
    print("=" * 80)
    print(f"Dataset   : {dataset_path.name}")
    print(f"Seed      : {args.seed} | So UAVs: {args.uavs} | Pop Size: {args.pop_size} | Iterations: {args.iterations}")
    print(f"Thuat toan: {args.algorithm}")
    print("-" * 80)

    # 1. Đọc và tiền xử lý dữ liệu
    df = load_users(dataset_path)
    validate_users(df)
    df = preprocess_users(df)
    ue_coords = df[["x_m", "y_m", "z_m"]].to_numpy()
    total_users = len(ue_coords)
    print(f"-> Da nap thanh cong {total_users} nguoi dung.")

    # 2. Khởi tạo bài toán UAV
    problem = UAVPlacementProblem(ue_coords=ue_coords, num_uavs=args.uavs)

    # 3. Lấy danh sách thuật toán
    optimizers = get_optimizers(args)
    results = {}
    detailed_metrics = {}

    print("\n--- Bat dau qua trinh toi uu hoa ---")
    for name, opt in optimizers.items():
        print(f"   > Dang chay {name:<12} ...", end="", flush=True)
        res = opt.optimize(problem)
        metrics = problem.evaluate_detailed(res.best_position)
        results[name] = res
        detailed_metrics[name] = metrics
        print(f" Hoan tat ({res.runtime_seconds:.2f}s) | Fitness: {res.best_objective:.4f} | Coverage: {metrics.coverage_rate*100:.1f}%")

    # 4. In bảng so sánh kết quả
    print("\n" + "=" * 80)
    print("BANG TONG HOP SO SANH KET QUA THUC NGHIEM")
    print("=" * 80)
    header = f"{'Thuat toan':<14} | {'Fitness':<9} | {'Coverage (f1)':<14} | {'Energy (f2)':<12} | {'Interf (f3)':<12} | {'UEs phu':<10} | {'Thoi gian':<8}"
    print(header)
    print("-" * 80)

    for name, res in results.items():
        m = detailed_metrics[name]
        row = (
            f"{name:<14} | "
            f"{res.best_objective:<9.4f} | "
            f"{m.coverage_rate * 100:>6.1f}%       | "
            f"{m.energy_normalized:>8.4f}     | "
            f"{m.interference_rate * 100:>6.1f}%      | "
            f"{m.covered_users_count:>3}/{m.total_users_count:<3}     | "
            f"{res.runtime_seconds:>6.2f}s"
        )
        print(row)
    print("=" * 80)

    # 5. Vẽ biểu đồ hội tụ nếu cần
    if not args.no_plot and len(results) > 0:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        plot_path = RESULTS_DIR / f"convergence_comparison_seed_{args.seed}_{dataset_path.stem}.png"

        plt.figure(figsize=(10, 6))
        for name, res in results.items():
            plt.plot(res.convergence_history, label=f"{name} (Best: {res.best_objective:.4f})", linewidth=2)

        plt.title(f"Đường cong hội tụ tối ưu vị trí UAV ({dataset_path.stem})", fontsize=14, fontweight="bold")
        plt.xlabel("Số vòng lặp (Iterations)", fontsize=12)
        plt.ylabel("Giá trị hàm thích nghi (Fitness - Maximize)", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig(plot_path, dpi=300)
        plt.close()
        print(f"\n📈 Đã lưu biểu đồ hội tụ tại: {plot_path}")


if __name__ == "__main__":
    main()
