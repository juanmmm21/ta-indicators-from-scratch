from __future__ import annotations

from ta_indicators_from_scratch.indicators import (
    bollinger_bands,
    ema,
    macd,
    rsi,
    sma,
)
from ta_indicators_from_scratch.models import IndicatorConfig, IndicatorResult
from ta_indicators_from_scratch.series import OhlcvSeries


class TechnicalAnalysisEngine:
    """Calcula indicadores clásicos sobre una serie OHLCV."""

    def __init__(self, config: IndicatorConfig | None = None) -> None:
        self._config = config or IndicatorConfig()

    @property
    def config(self) -> IndicatorConfig:
        return self._config

    def compute_sma(self, series: OhlcvSeries, period: int | None = None) -> IndicatorResult:
        selected_period = period or self._config.sma_period
        values = sma(series.close, selected_period)
        return IndicatorResult(name="sma", values={"sma": values})

    def compute_ema(self, series: OhlcvSeries, period: int | None = None) -> IndicatorResult:
        selected_period = period or self._config.ema_period
        values = ema(series.close, selected_period)
        return IndicatorResult(name="ema", values={"ema": values})

    def compute_rsi(self, series: OhlcvSeries, period: int | None = None) -> IndicatorResult:
        selected_period = period or self._config.rsi_period
        values = rsi(series.close, selected_period)
        return IndicatorResult(name="rsi", values={"rsi": values})

    def compute_macd(self, series: OhlcvSeries) -> IndicatorResult:
        result = macd(
            series.close,
            fast_period=self._config.macd_fast,
            slow_period=self._config.macd_slow,
            signal_period=self._config.macd_signal,
        )
        return IndicatorResult(
            name="macd",
            values={
                "macd_line": result.macd_line,
                "signal_line": result.signal_line,
                "histogram": result.histogram,
            },
        )

    def compute_bollinger(self, series: OhlcvSeries) -> IndicatorResult:
        result = bollinger_bands(
            series.close,
            period=self._config.bollinger_period,
            num_std=self._config.bollinger_std,
        )
        return IndicatorResult(
            name="bollinger",
            values={
                "middle_band": result.middle_band,
                "upper_band": result.upper_band,
                "lower_band": result.lower_band,
            },
        )

    def compute_all(self, series: OhlcvSeries) -> dict[str, IndicatorResult]:
        return {
            "sma": self.compute_sma(series),
            "ema": self.compute_ema(series),
            "rsi": self.compute_rsi(series),
            "macd": self.compute_macd(series),
            "bollinger": self.compute_bollinger(series),
        }
