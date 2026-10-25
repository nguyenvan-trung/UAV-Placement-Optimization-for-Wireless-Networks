"""Geometric constraints; minimum distance is a simulation assumption."""
import numpy as np


def satisfies_minimum_separation(coords: np.ndarray, minimum: float) -> bool:
    distances = np.linalg.norm(coords[:, None, :] - coords[None, :, :], axis=-1)
    return bool(np.all(distances[np.triu_indices(len(coords), k=1)] >= minimum))
