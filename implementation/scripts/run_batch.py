"""Chạy hàng loạt (Batch Runner) các thuật toán trên nhiều bộ dữ liệu."""

import argparse
import sys
import time
from pathlib import Path

IMPLEMENTATION_DIR = Path(__file__).resolve().parents[1]
if str(IMPLEMENTATION_DIR) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_DIR))

# Thiết lập UTF-8 để tương thích console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

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
    parser = argparse.ArgumentParser(description="Chạy hàng loạt trên nhiều file CSV trong data/stores.")
    parser.add_argument(
        "--mode",
        choices=("representative", "all", "custom"),
        default="representative",
        help="Chế độ: 'representative' (chọn đại diện từng mức 50->500 users), 'all' (cả 500 file), 'custom'.",
    )
    parser.add_argument("--uavs", type=int, default=DEFAULT_NUM_UAVS, help="Số lượng UAV.")
    parser.add_argument("--pop-size", type=int, default=25, help="Kích thước quần thể.")
    parser.add_argument("--iterations", type=int, default=30, help="Số vòng lặp.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument(
        "--algorithms",
        nargs="+",
        default=["GA", "PSO", "WOA", "H-PSO-GA", "H-WOA-PSO", "I-WOA"],
        help="Danh sách thuật toán cần chạy.",
    )
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn tối đa số file CSV chạy.")
    return parser.parse_args()


def select_datasets(mode: str, limit: int | None = None) -> list[Path]:
    all_files = sorted(DATASET_STORES_DIR.glob("*_users_connect.csv"))
    if not all_files:
        print(f"Lỗi: Không tìm thấy file CSV nào trong {DATASET_STORES_DIR}")
        sys.exit(1)

    if mode == "all":
        selected = all_files
    elif mode == "representative":
        # Chọn 10 file đại diện cho 10 mức quy mô: 50, 100, 150, 200, 250, 300, 350, 400, 450, 500
        # Tương ứng với các file từ 001 đến 010
        selected = all_files[:10]
    else:
        selected = all_files[:limit] if limit else all_files[:5]

    if limit is not None:
        selected = selected[:limit]

    return selected


def main() -> None:
    args = parse_args()
    files = select_datasets(args.mode, args.limit)

    print("=" * 85)
    print("CHẠY HÀNG LOẠT (BATCH RUNNER) TRÊN BỘ DỮ LIỆU UAV")
    print(f"Chế độ      : {args.mode}")
    print(f"Số lượng file: {len(files)} / {len(list(DATASET_STORES_DIR.glob('*_users_connect.csv')))} files")
    print(f"Thuật toán  : {args.algorithms}")
    print(f"Cấu hình    : UAVs={args.uavs} | PopSize={args.pop_size} | Iterations={args.iterations} | Seed={args.seed}")
    print("=" * 85)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    out_csv = RESULTS_DIR / f"batch_results_{args.mode}_{int(time.time())}.csv"

    records = []

    for idx, fpath in enumerate(files, 1):
        print(f"\n[{idx}/{len(files)}] Đang xử lý: {fpath.name}")
        df = load_users(fpath)
        validate_users(df)
        df = preprocess_users(df)
        ue_coords = df[["x_m", "y_m", "z_m"]].to_numpy()
        total_users = len(ue_coords)

        problem = UAVPlacementProblem(ue_coords=ue_coords, num_uavs=args.uavs)

        algo_factories = {
            "GA": lambda: GAOptimizer(GAParameters(population_size=args.pop_size, generations=args.iterations), seed=args.seed),
            "PSO": lambda: PSOOptimizer(PSOParameters(swarm_size=args.pop_size, iterations=args.iterations), seed=args.seed),
            "WOA": lambda: WOAOptimizer(WOAParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
            "H-PSO-GA": lambda: HybridPSOGAOptimizer(HPSOGAParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
            "H-WOA-PSO": lambda: HybridWOAPSOOptimizer(HWOAPSOParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
            "I-WOA": lambda: IWOAOptimizer(IWOAParameters(population_size=args.pop_size, iterations=args.iterations), seed=args.seed),
        }

        for algo_name in args.algorithms:
            if algo_name not in algo_factories:
                continue
            opt = algo_factories[algo_name]()
            res = opt.optimize(problem)
            m = problem.evaluate_detailed(res.best_position)

            records.append({
                "Dataset": fpath.name,
                "Total_Users": total_users,
                "Num_UAVs": args.uavs,
                "Algorithm": algo_name,
                "Fitness": res.best_objective,
                "Coverage_Rate": m.coverage_rate,
                "Covered_Users": m.covered_users_count,
                "Energy_Normalized": m.energy_normalized,
                "Interference_Rate": m.interference_rate,
                "Runtime_Seconds": res.runtime_seconds,
            })
            print(f"   > {algo_name:<11} | Fit: {res.best_objective:.4f} | Cov: {m.coverage_rate*100:>5.1f}% | Time: {res.runtime_seconds:.2f}s")

        # Lưu trung gian sau mỗi file đề phòng gián đoạn
        pd.DataFrame(records).to_csv(out_csv, index=False)

    print("\n" + "=" * 85)
    print(f"HOÀN TẤT BATCH RUN! Đã lưu toàn bộ dữ liệu thực nghiệm tại:\n-> {out_csv}")
    print("=" * 85)


if __name__ == "__main__":
    main()
