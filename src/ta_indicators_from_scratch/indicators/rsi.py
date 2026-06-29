from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ta_indicators_from_scratch.models import validate_period


def rsi(values: npt.NDArray[np.float64], period: int = 14) -> npt.NDArray[np.float64]:
    """Relative Strength Index con suavizado de Wilder."""
    validate_period(period)
    result = np.full(values.shape, np.nan, dtype=np.float64)
    if values.size <= period:
        return result

    deltas = np.diff(values)
    gains = np.where(deltas > 0.0, deltas, 0.0)
    losses = np.where(deltas < 0.0, -deltas, 0.0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    if avg_loss == 0.0:
        result[period] = 100.0
    else:
        rs = avg_gain / avg_loss
        result[period] = 100.0 - (100.0 / (1.0 + rs))

    for index in range(period + 1, values.size):
        gain = gains[index - 1]
        loss = losses[index - 1]
        avg_gain = ((avg_gain * (period - 1)) + gain) / period
        avg_loss = ((avg_loss * (period - 1)) + loss) / period

        if avg_loss == 0.0:
            result[index] = 100.0
            continue

        rs = avg_gain / avg_loss
        result[index] = 100.0 - (100.0 / (1.0 + rs))

    return result
