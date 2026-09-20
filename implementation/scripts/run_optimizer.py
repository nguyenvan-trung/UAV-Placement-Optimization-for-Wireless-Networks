"""Điểm chạy thuật toán tối ưu vị trí UAV."""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UAV placement optimization")
    parser.add_argument("--algorithm", choices=("GA", "PSO", "WOA", "all"), default="all")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dataset", type=str, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"Algorithm: {args.algorithm} | Seed: {args.seed} | Dataset: {args.dataset}")
    print("Project scaffold is ready; implement the objective and optimizers before optimization.")


if __name__ == "__main__":
    main()
