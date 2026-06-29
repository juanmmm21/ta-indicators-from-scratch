from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ta_indicators_from_scratch.models import validate_period


def ema(values: npt.NDArray[np.float64], period: int) -> npt.NDArray[np.float64]:
    """Exponential Moving Average con semilla SMA en el primer valor válido."""
    validate_period(period)
    result = np.full(values.shape, np.nan, dtype=np.float64)
    if values.size < period:
        return result

    alpha = 2.0 / (period + 1.0)
    seed_index = period - 1
    result[seed_index] = np.mean(values[:period])

    for index in range(seed_index + 1, values.size):
        previous = result[index - 1]
        result[index] = alpha * values[index] + (1.0 - alpha) * previous

    return result
