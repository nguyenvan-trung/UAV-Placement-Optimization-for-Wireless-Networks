"""Chạy thí nghiệm Monte Carlo nhiều seed, tổng hợp thống kê và kiểm định Wilcoxon."""

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
from scipy.stats import ranksums

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
from src.constants.experiment import DEFAULT_SEEDS
from src.constants.network import DEFAULT_NUM_UAVS
from src.constants.paths import RESULTS_DIR
from src.input.data_loader import load_users
from src.input.data_validator import validate_users
from src.preprocessing.preprocessor import preprocess_users
from src.problem.objective import UAVPlacementProblem


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chạy thí nghiệm so sánh nhiều seed (Monte Carlo).")
    parser.add_argument("--dataset", type=str, default="data/stores/001_UAV_3D_50_users_connect.csv")
    parser.add_argument("--uavs", type=int, default=DEFAULT_NUM_UAVS)
    parser.add_argument("--pop-size", type=int, default=25)
    parser.add_argument("--iterations", type=int, default=30)
    parser.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    return parser.parse_args()


def run_experiment(args: argparse.Namespace) -> None:
    dataset_path = Path(args.dataset)
    if not dataset_path.is_absolute():
        dataset_path = (Path.cwd() / dataset_path).resolve()

    df = load_users(dataset_path)
    validate_users(df)
    df = preprocess_users(df)
    ue_coords = df[["x_m", "y_m", "z_m"]].to_numpy()

    problem = UAVPlacementProblem(ue_coords=ue_coords, num_uavs=args.uavs)

    algo_factories = {
        "GA": lambda s: GAOptimizer(GAParameters(population_size=args.pop_size, generations=args.iterations), seed=s),
        "PSO": lambda s: PSOOptimizer(PSOParameters(swarm_size=args.pop_size, iterations=args.iterations), seed=s),
        "WOA": lambda s: WOAOptimizer(WOAParameters(population_size=args.pop_size, iterations=args.iterations), seed=s),
        "H-PSO-GA": lambda s: HybridPSOGAOptimizer(HPSOGAParameters(population_size=args.pop_size, iterations=args.iterations), seed=s),
        "H-WOA-PSO": lambda s: HybridWOAPSOOptimizer(HWOAPSOParameters(population_size=args.pop_size, iterations=args.iterations), seed=s),
        "I-WOA": lambda s: IWOAOptimizer(IWOAParameters(population_size=args.pop_size, iterations=args.iterations), seed=s),
    }

    records = []
    convergence_histories = {name: [] for name in algo_factories}

    print("=" * 80)
    print("THI NGHIEM MONTE CARLO SO SANH TOAN DIEN CAC THUAT TOAN")
    print(f"Dataset: {dataset_path.name} | UAVs: {args.uavs} | Seeds: {args.seeds}")
    print("=" * 80)

    for seed in args.seeds:
        print(f"\n--- Dang chay Seed: {seed} ---")
        for name, factory in algo_factories.items():
            opt = factory(seed)
            res = opt.optimize(problem)
            metrics = problem.evaluate_detailed(res.best_position)
            convergence_histories[name].append(res.convergence_history)

            records.append({
                "Algorithm": name,
                "Seed": seed,
                "Fitness": res.best_objective,
                "Coverage_f1": metrics.coverage_rate,
                "Energy_f2": metrics.energy_normalized,
                "Interference_f3": metrics.interference_rate,
                "Runtime_s": res.runtime_seconds,
            })
            print(f"   {name:<12} | Fitness: {res.best_objective:.4f} | Coverage: {metrics.coverage_rate*100:.1f}%")

    results_df = pd.DataFrame(records)

    # Thống kê tổng hợp Mean +/- Std
    summary = results_df.groupby("Algorithm").agg(
        Fitness_Mean=("Fitness", "mean"),
        Fitness_Std=("Fitness", "std"),
        Coverage_Mean=("Coverage_f1", "mean"),
        Energy_Mean=("Energy_f2", "mean"),
        Interference_Mean=("Interference_f3", "mean"),
        Runtime_Mean=("Runtime_s", "mean"),
    ).reset_index()

    # Kiểm định thống kê Wilcoxon Rank-Sum so với I-WOA
    iwoa_scores = results_df[results_df["Algorithm"] == "I-WOA"]["Fitness"].to_numpy()
    p_values = {}
    for name in algo_factories:
        if name == "I-WOA":
            p_values[name] = 1.0
            continue
        scores = results_df[results_df["Algorithm"] == name]["Fitness"].to_numpy()
        try:
            stat, p_val = ranksums(iwoa_scores, scores)
            p_values[name] = p_val
        except Exception:
            p_values[name] = np.nan

    summary["Wilcoxon_p_value"] = summary["Algorithm"].map(p_values)

    print("\n" + "=" * 90)
    print("BANG TONG HOP THONG KE QUA CAC SEED & KIEM DINH WILCOXON")
    print("=" * 90)
    print(summary.to_string(index=False))
    print("=" * 90)

    # Lưu kết quả
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = RESULTS_DIR / f"monte_carlo_summary_{dataset_path.stem}.csv"
    summary.to_csv(csv_path, index=False)
    print(f"\nDa luu bang ket qua thong ke tai: {csv_path}")

    # Vẽ biểu đồ hội tụ trung bình
    plt.figure(figsize=(10, 6))
    for name, histories in convergence_histories.items():
        arr = np.array(histories)
        mean_curve = np.mean(arr, axis=0)
        plt.plot(mean_curve, label=name, linewidth=2)

    plt.title(f"Hoi tu trung binh qua cac seed ({dataset_path.stem})", fontsize=14, fontweight="bold")
    plt.xlabel("Iterations", fontsize=12)
    plt.ylabel("Fitness (Maximize)", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend(fontsize=11)
    plt.tight_layout()
    plot_path = RESULTS_DIR / f"monte_carlo_convergence_{dataset_path.stem}.png"
    plt.savefig(plot_path, dpi=300)
    plt.close()
    print(f"Da luu bieu do hoi tu Monte Carlo tai: {plot_path}")


def main() -> None:
    args = parse_args()
    run_experiment(args)


if __name__ == "__main__":
    main()
