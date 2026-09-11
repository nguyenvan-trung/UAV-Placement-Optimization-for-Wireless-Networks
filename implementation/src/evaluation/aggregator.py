"""Tổng hợp mean, standard deviation, best và worst theo nhiều seed."""

import pandas as pd


def summarize(results: pd.DataFrame) -> pd.DataFrame:
    metrics = ["coverage", "best_objective", "runtime_seconds"]
    return results.groupby("algorithm")[metrics].agg(["mean", "std", "min", "max"])
