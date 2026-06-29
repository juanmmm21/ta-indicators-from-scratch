from __future__ import annotations

import numpy as np
import pytest

from ta_indicators_from_scratch.indicators.bollinger import bollinger_bands
from ta_indicators_from_scratch.indicators.sma import sma


def test_bollinger_middle_matches_sma() -> None:
    values = np.linspace(100.0, 120.0, num=40, dtype=np.float64)
    bands = bollinger_bands(values, period=20, num_std=2.0)
    expected_middle = sma(values, period=20)

    assert np.allclose(bands.middle_band, expected_middle, equal_nan=True)
    assert bands.upper_band[-1] > bands.middle_band[-1]
    assert bands.lower_band[-1] < bands.middle_band[-1]


def test_bollinger_rejects_invalid_std() -> None:
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    with pytest.raises(ValueError):
        bollinger_bands(values, period=3, num_std=0.0)
