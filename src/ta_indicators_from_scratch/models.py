from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True, slots=True)
class IndicatorResult:
    """Salida normalizada de un indicador técnico."""

    name: str
    values: dict[str, npt.NDArray[np.float64]]

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("name must not be empty")
        if not self.values:
            raise ValueError("values must not be empty")
        lengths = {len(series) for series in self.values.values()}
        if len(lengths) != 1:
            raise ValueError("all output series must share the same length")


@dataclass(frozen=True, slots=True)
class MacdResult:
    macd_line: npt.NDArray[np.float64]
    signal_line: npt.NDArray[np.float64]
    histogram: npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class BollingerResult:
    middle_band: npt.NDArray[np.float64]
    upper_band: npt.NDArray[np.float64]
    lower_band: npt.NDArray[np.float64]


@dataclass(frozen=True, slots=True)
class IndicatorConfig:
    sma_period: int = 20
    ema_period: int = 20
    rsi_period: int = 14
    macd_fast: int = 12
    macd_slow: int = 26
    macd_signal: int = 9
    bollinger_period: int = 20
    bollinger_std: float = 2.0

    def __post_init__(self) -> None:
        if self.sma_period <= 0:
            raise ValueError("sma_period must be positive")
        if self.ema_period <= 0:
            raise ValueError("ema_period must be positive")
        if self.rsi_period <= 0:
            raise ValueError("rsi_period must be positive")
        if self.macd_fast <= 0 or self.macd_slow <= 0 or self.macd_signal <= 0:
            raise ValueError("macd periods must be positive")
        if self.macd_fast >= self.macd_slow:
            raise ValueError("macd_fast must be lower than macd_slow")
        if self.bollinger_period <= 0:
            raise ValueError("bollinger_period must be positive")
        if self.bollinger_std <= 0:
            raise ValueError("bollinger_std must be positive")


def validate_period(period: int, name: str = "period") -> None:
    if period <= 0:
        raise ValueError(f"{name} must be positive")


def as_float64_array(values: npt.ArrayLike, name: str = "values") -> npt.NDArray[np.float64]:
    array = np.asarray(values, dtype=np.float64)
    if array.ndim != 1:
        raise ValueError(f"{name} must be a one-dimensional array")
    if array.size == 0:
        raise ValueError(f"{name} must not be empty")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} must contain only finite numbers")
    return array


def records_to_arrays(records: list[dict[str, Any]]) -> dict[str, npt.NDArray[np.float64]]:
    if not records:
        raise ValueError("records must not be empty")
    required = ("open", "high", "low", "close", "volume")
    for field in required:
        if field not in records[0]:
            raise ValueError(f"missing required field: {field}")
    return {
        field: as_float64_array([row[field] for row in records], name=field) for field in required
    }
