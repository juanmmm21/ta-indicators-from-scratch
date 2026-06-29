from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ta_indicators_from_scratch.models import validate_period


def sma(values: npt.NDArray[np.float64], period: int) -> npt.NDArray[np.float64]:
    """Simple Moving Average usando convolución vectorizada."""
    validate_period(period)
    result = np.full(values.shape, np.nan, dtype=np.float64)
    if values.size < period:
        return result

    kernel = np.ones(period, dtype=np.float64) / period
    rolling = np.convolve(values, kernel, mode="valid")
    result[period - 1 :] = rolling
    return result


def rolling_std(values: npt.NDArray[np.float64], period: int) -> npt.NDArray[np.float64]:
    """Desviación estándar móvil con ventana deslizante."""
    validate_period(period)
    result = np.full(values.shape, np.nan, dtype=np.float64)
    if values.size < period:
        return result

    for index in range(period - 1, values.size):
        window = values[index - period + 1 : index + 1]
        result[index] = np.std(window, ddof=0)
    return result
