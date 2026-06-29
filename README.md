# ta-indicators-from-scratch

NumPy-vectorized **technical analysis library** implementing classic indicators from scratch — without TA-Lib or third-party TA packages. Fourth module of the [quant-core-infra](https://github.com/juanmmm21/quant-core-infra) ecosystem, consuming OHLCV candles produced by `market-data-lakehouse`.

Repository: [github.com/juanmmm21/ta-indicators-from-scratch](https://github.com/juanmmm21/ta-indicators-from-scratch)

---

## Objective

This project demonstrates:

- Exact financial mathematics behind standard indicators
- Vectorized NumPy operations for statistical throughput
- Clean, composable indicator APIs with typed outputs
- JSONL candle ingestion compatible with lakehouse exports

---

## Supported indicators

| Indicator | Function | Default parameters |
|-----------|----------|--------------------|
| **SMA** | Simple Moving Average | period `20` |
| **EMA** | Exponential Moving Average | period `20` |
| **RSI** | Relative Strength Index (Wilder) | period `14` |
| **MACD** | MACD line, signal, histogram | `12 / 26 / 9` |
| **Bollinger Bands** | Middle, upper, lower bands | period `20`, σ `2.0` |

All indicators return `NaN` during the warmup window until enough candles are available.

---

## Architecture

```text
OHLCV candles (JSONL / arrays)
        │
        ▼
OhlcvSeries
        │
        ▼
TechnicalAnalysisEngine
   ├─ sma / ema / rsi
   ├─ macd
   └─ bollinger_bands
        │
        ▼
IndicatorResult (typed NumPy arrays)
```

### Core components

| Module | Responsibility |
|--------|----------------|
| `series.py` | Normalized OHLCV container and record parsing |
| `indicators/sma.py` | SMA via convolution + rolling standard deviation |
| `indicators/ema.py` | EMA with SMA seed |
| `indicators/rsi.py` | RSI with Wilder smoothing |
| `indicators/macd.py` | MACD crossover stack |
| `indicators/bollinger.py` | Bollinger Bands around SMA |
| `engine.py` | Orchestrates indicator computation |
| `pipeline.py` | JSONL ingest + CLI output serialization |

### Technical decisions

- **float64 arrays** for indicator math (acceptable for pure statistical TA per ecosystem rules)
- **No pandas / TA-Lib** — only NumPy to keep dependencies minimal
- **Explicit warmup NaNs** so downstream strategies can gate on data readiness
- **JSONL compatibility** with `market-data-lakehouse` candle exports

---

## Requirements

- Python **3.11+**

---

## Installation

```bash
cd ta-indicators-from-scratch
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## CLI usage

### Compute all indicators

```bash
ta-indicators-from-scratch compute \
  --input samples/btcusdt_1m_candles.jsonl \
  --indicator all
```

### Compute a single indicator

```bash
ta-indicators-from-scratch compute \
  --input samples/btcusdt_1m_candles.jsonl \
  --indicator rsi \
  --rsi-period 14
```

---

## JSONL candle format

Each line is one OHLCV candle:

```json
{
  "open": 100.5,
  "high": 101.0,
  "low": 99.5,
  "close": 100.8,
  "volume": 12.0
}
```

---

## Programmatic usage

```python
import numpy as np

from ta_indicators_from_scratch import OhlcvSeries, TechnicalAnalysisEngine, rsi, sma

close = np.linspace(100.0, 130.0, num=60, dtype=np.float64)
series = OhlcvSeries.from_arrays(
    open_=close - 0.5,
    high=close + 1.0,
    low=close - 1.0,
    close=close,
    volume=np.full(60, 10.0),
)

engine = TechnicalAnalysisEngine()
results = engine.compute_all(series)

standalone_rsi = rsi(series.close, period=14)
standalone_sma = sma(series.close, period=20)
```

---

## Development

```bash
pytest -q
ruff check src tests
mypy src
```

---

## Ecosystem integration

```text
market-data-lakehouse → ta-indicators-from-scratch → alpha-signal-generator
```

---

## License

MIT
