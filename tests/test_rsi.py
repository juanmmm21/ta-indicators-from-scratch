from __future__ import annotations

import numpy as np
import pytest

from ta_indicators_from_scratch.indicators.rsi import rsi


def test_rsi_bounds_and_warmup() -> None:
    values = np.linspace(100.0, 120.0, num=30, dtype=np.float64)
    result = rsi(values, period=14)

    assert np.isnan(result[:14]).all()
    valid = result[14:]
    assert np.all(valid >= 0.0)
    assert np.all(valid <= 100.0)


def test_rsi_uptrend_is_high() -> None:
    values = np.arange(1.0, 31.0, dtype=np.float64)
    result = rsi(values, period=14)
    assert result[-1] == pytest.approx(100.0)
