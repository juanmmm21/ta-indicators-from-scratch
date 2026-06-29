from __future__ import annotations

import numpy as np
import pytest

from ta_indicators_from_scratch.indicators.sma import sma
from ta_indicators_from_scratch.models import validate_period


def test_sma_period_three() -> None:
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)
    result = sma(values, period=3)

    assert np.isnan(result[:2]).all()
    assert result[2] == pytest.approx(2.0)
    assert result[3] == pytest.approx(3.0)
    assert result[4] == pytest.approx(4.0)


def test_sma_rejects_invalid_period() -> None:
    values = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    with pytest.raises(ValueError):
        sma(values, period=0)


def test_validate_period() -> None:
    with pytest.raises(ValueError):
        validate_period(0)
