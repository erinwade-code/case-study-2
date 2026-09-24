import numpy as np


def apply_mask(values: np.ndarray, threshold: float) -> np.ndarray:
    """Return values greater than the threshold."""
    mask = values > threshold
    return values[mask]


def vectorized_calculation(values: np.ndarray) -> np.ndarray:
    """Calculate 10% of each value using NumPy."""
    return values * 0.10


def loop_calculation(values: np.ndarray) -> np.ndarray:
    """Calculate 10% of each value using a Python loop."""
    result = []

    for value in values:
        result.append(value * 0.10)

    return np.array(result)


def aggregate_values(values: np.ndarray) -> float:
    """Return the sum of the values."""
    return float(np.sum(values))