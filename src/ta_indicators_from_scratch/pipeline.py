from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np

from ta_indicators_from_scratch.engine import TechnicalAnalysisEngine
from ta_indicators_from_scratch.models import IndicatorConfig
from ta_indicators_from_scratch.series import OhlcvSeries


def load_candle_records(path: str | Path) -> list[dict[str, Any]]:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"candle file not found: {file_path}")

    records: list[dict[str, Any]] = []
    with file_path.open("r", encoding="utf-8") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            line = raw_line.strip()
            if not line:
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid json on line {line_number}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"line {line_number} must contain a JSON object")
            records.append(payload)

    if not records:
        raise ValueError("candle file is empty")
    return records


def _sanitize_series(values: np.ndarray) -> list[float | None]:
    sanitized: list[float | None] = []
    for value in values:
        if np.isnan(value):
            sanitized.append(None)
        else:
            sanitized.append(float(value))
    return sanitized


def serialize_indicator_output(
    series: OhlcvSeries,
    results: dict[str, Any],
) -> dict[str, Any]:
    output: dict[str, Any] = {
        "length": series.length,
        "ohlcv": series.to_dict(),
        "indicators": {},
    }

    for name, result in results.items():
        if hasattr(result, "values"):
            output["indicators"][name] = {
                key: _sanitize_series(array) for key, array in result.values.items()
            }
        else:
            output["indicators"][name] = result

    return output


def run_compute(
    input_path: str,
    indicator: str,
    config: IndicatorConfig,
) -> dict[str, Any]:
    records = load_candle_records(input_path)
    series = OhlcvSeries.from_records(records)
    engine = TechnicalAnalysisEngine(config)

    if indicator == "all":
        results = engine.compute_all(series)
        return serialize_indicator_output(series, results)

    dispatch = {
        "sma": engine.compute_sma,
        "ema": engine.compute_ema,
        "rsi": engine.compute_rsi,
        "macd": engine.compute_macd,
        "bollinger": engine.compute_bollinger,
    }
    if indicator not in dispatch:
        raise ValueError(f"unsupported indicator: {indicator}")

    result = dispatch[indicator](series)
    return serialize_indicator_output(series, {indicator: result})
