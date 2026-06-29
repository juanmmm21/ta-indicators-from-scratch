from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from ta_indicators_from_scratch.engine import TechnicalAnalysisEngine
from ta_indicators_from_scratch.models import IndicatorConfig
from ta_indicators_from_scratch.pipeline import load_candle_records, run_compute
from ta_indicators_from_scratch.series import OhlcvSeries


def _sample_series() -> OhlcvSeries:
    close = np.linspace(100.0, 130.0, num=40, dtype=np.float64)
    return OhlcvSeries.from_arrays(
        open_=close - 0.5,
        high=close + 1.0,
        low=close - 1.0,
        close=close,
        volume=np.full(40, 10.0, dtype=np.float64),
    )


def test_ohlcv_series_validation() -> None:
    close = np.array([1.0, 2.0, 3.0], dtype=np.float64)
    with pytest.raises(ValueError):
        OhlcvSeries.from_arrays(
            open_=close,
            high=close,
            low=close,
            close=close,
            volume=np.array([1.0, 2.0], dtype=np.float64),
        )


def test_engine_compute_all() -> None:
    engine = TechnicalAnalysisEngine()
    results = engine.compute_all(_sample_series())

    assert set(results) == {"sma", "ema", "rsi", "macd", "bollinger"}
    assert len(results["rsi"].values["rsi"]) == 40


def test_pipeline_with_sample_file(tmp_path: Path) -> None:
    sample_path = Path(__file__).resolve().parents[1] / "samples" / "btcusdt_1m_candles.jsonl"
    records = load_candle_records(sample_path)
    output_path = tmp_path / "indicators.json"

    payload = run_compute(str(sample_path), indicator="rsi", config=IndicatorConfig())
    assert payload["length"] == len(records)

    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle)

    assert output_path.exists()
