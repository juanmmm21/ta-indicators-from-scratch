from __future__ import annotations

import numpy as np
import pytest

from ta_indicators_from_scratch.indicators.ema import ema


def test_ema_period_three() -> None:
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    result = ema(values, period=3)

    assert np.isnan(result[:2]).all()
    assert result[2] == pytest.approx(2.0)
    assert result[3] == pytest.approx(3.0)
    assert result[4] == pytest.approx(4.0)
