from __future__ import annotations

import numpy as np

from ta_indicators_from_scratch.indicators.macd import macd


def test_macd_output_shapes() -> None:
    values = np.linspace(100.0, 130.0, num=60, dtype=np.float64)
    result = macd(values, fast_period=12, slow_period=26, signal_period=9)

    assert len(result.macd_line) == len(values)
    assert len(result.signal_line) == len(values)
    assert len(result.histogram) == len(values)
    assert np.isnan(result.macd_line[:25]).all()
    assert np.isnan(result.histogram[:33]).all()
    assert np.isfinite(result.histogram[-1])
