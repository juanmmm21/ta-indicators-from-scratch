from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import numpy.typing as npt

from ta_indicators_from_scratch.models import as_float64_array, records_to_arrays


@dataclass(frozen=True, slots=True)
class OhlcvSeries:
    """Serie OHLCV homogénea para alimentar indicadores técnicos."""

    open: npt.NDArray[np.float64]
    high: npt.NDArray[np.float64]
    low: npt.NDArray[np.float64]
    close: npt.NDArray[np.float64]
    volume: npt.NDArray[np.float64]

    def __post_init__(self) -> None:
        length = len(self.close)
        for field_name, array in (
            ("open", self.open),
            ("high", self.high),
            ("low", self.low),
            ("volume", self.volume),
        ):
            if len(array) != length:
                raise ValueError(f"{field_name} length must match close length")

    @property
    def length(self) -> int:
        return len(self.close)

    @classmethod
    def from_arrays(
        cls,
        open_: npt.ArrayLike,
        high: npt.ArrayLike,
        low: npt.ArrayLike,
        close: npt.ArrayLike,
        volume: npt.ArrayLike,
    ) -> OhlcvSeries:
        return cls(
            open=as_float64_array(open_, name="open"),
            high=as_float64_array(high, name="high"),
            low=as_float64_array(low, name="low"),
            close=as_float64_array(close, name="close"),
            volume=as_float64_array(volume, name="volume"),
        )

    @classmethod
    def from_records(cls, records: list[dict[str, Any]]) -> OhlcvSeries:
        arrays = records_to_arrays(records)
        return cls(
            open=arrays["open"],
            high=arrays["high"],
            low=arrays["low"],
            close=arrays["close"],
            volume=arrays["volume"],
        )

    def to_dict(self) -> dict[str, list[float | None]]:
        return {
            "open": self.open.tolist(),
            "high": self.high.tolist(),
            "low": self.low.tolist(),
            "close": self.close.tolist(),
            "volume": self.volume.tolist(),
        }
