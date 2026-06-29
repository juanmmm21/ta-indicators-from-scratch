from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ta_indicators_from_scratch.indicators.ema import ema
from ta_indicators_from_scratch.models import MacdResult, validate_period


def macd(
    values: npt.NDArray[np.float64],
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> MacdResult:
    """MACD clásico: EMA rápida - EMA lenta, señal EMA y histograma."""
    validate_period(fast_period, name="fast_period")
    validate_period(slow_period, name="slow_period")
    validate_period(signal_period, name="signal_period")
    if fast_period >= slow_period:
        raise ValueError("fast_period must be lower than slow_period")

    fast_ema = ema(values, fast_period)
    slow_ema = ema(values, slow_period)
    macd_line = fast_ema - slow_ema

    signal_line = np.full(values.shape, np.nan, dtype=np.float64)
    valid_start = slow_period - 1
    if values.size > valid_start:
        signal_segment = ema(macd_line[valid_start:], signal_period)
        signal_line[valid_start:] = signal_segment

    histogram = macd_line - signal_line

    return MacdResult(
        macd_line=macd_line,
        signal_line=signal_line,
        histogram=histogram,
    )
