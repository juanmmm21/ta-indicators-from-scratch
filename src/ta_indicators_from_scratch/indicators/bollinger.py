from __future__ import annotations

import numpy as np
import numpy.typing as npt

from ta_indicators_from_scratch.indicators.sma import rolling_std, sma
from ta_indicators_from_scratch.models import BollingerResult, validate_period


def bollinger_bands(
    values: npt.NDArray[np.float64],
    period: int = 20,
    num_std: float = 2.0,
) -> BollingerResult:
    """Bandas de Bollinger: SMA central ± desviación estándar móvil."""
    validate_period(period)
    if num_std <= 0.0:
        raise ValueError("num_std must be positive")

    middle_band = sma(values, period)
    std = rolling_std(values, period)
    offset = num_std * std

    return BollingerResult(
        middle_band=middle_band,
        upper_band=middle_band + offset,
        lower_band=middle_band - offset,
    )
