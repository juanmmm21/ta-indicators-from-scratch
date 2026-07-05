# ta-indicators-from-scratch

**Vectorized technical analysis** library that implements classic indicators from scratch with NumPy — no TA-Lib, pandas-ta, or third-party dependencies. Fourth module of the [quant-core-infra](https://github.com/juanmmm21/quant-core-infra) ecosystem.

Repository: [github.com/juanmmm21/ta-indicators-from-scratch](https://github.com/juanmmm21/ta-indicators-from-scratch)

---

## What it is and what problem it solves

Indicator libraries (TA-Lib, etc.) are black boxes: they return a number without the developer understanding the exact math. In a quantitative portfolio that's a problem: you can't audit, optimize, or explain the signals.

This project implements the formulas **explicitly** using vectorized NumPy operations:

- You know exactly what happens in each warmup window
- You can compose indicators into your own pipelines
- Performance stays at C level thanks to vectorization

Consumes OHLCV candles from `market-data-lakehouse` and feeds `alpha-signal-generator`.

---

## Role in quant-core-infra

```text
market-data-lakehouse ──► OHLCV candles ──► ta-indicators-from-scratch ──► indicators
                                                    │
                                          alpha-signal-generator
```

Translates **historical price** into **statistical features** that strategies evaluate bar by bar.

---

## Supported indicators

| Indicator | Function | Default parameters | Key formula |
|-----------|---------|------------------------|---------------|
| **SMA** | Simple moving average | period `20` | Arithmetic mean of N closes |
| **EMA** | Exponential moving average | period `20` | `α = 2/(N+1)`, SMA seed |
| **RSI** | Relative strength index | period `14` | Wilder's smoothing over gains/losses |
| **MACD** | Convergence/divergence | `12 / 26 / 9` | Fast EMA − slow EMA, signal EMA |
| **Bollinger** | Volatility bands | period `20`, σ `2.0` | Rolling SMA ± k·σ |

All return `NaN` during the warmup window until enough candles have accumulated.

---

## How it works

1. **Input:** `float64` arrays or JSONL with OHLCV fields.
2. **Container:** `OhlcvSeries` validates lengths and finite values.
3. **Calculation:** each indicator is a pure `ndarray → ndarray` function.
4. **Engine:** `TechnicalAnalysisEngine` orchestrates all indicators over the same series.
5. **Output:** `IndicatorResult` with arrays aligned by candle index.
6. **CLI:** serializes to JSON with `null` wherever there's a `NaN`.

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
   ├─ macd (line, signal, histogram)
   └─ bollinger_bands (mean, upper, lower)
        │
        ▼
IndicatorResult
```

### Components

| Module | Responsibility |
|--------|----------------|
| `series.py` | OHLCV container and record parsing |
| `indicators/sma.py` | SMA via convolution + rolling std |
| `indicators/ema.py` | EMA with SMA seed |
| `indicators/rsi.py` | Wilder RSI |
| `indicators/macd.py` | Full MACD stack |
| `indicators/bollinger.py` | Bands around SMA |
| `engine.py` | Multi-indicator orchestration |
| `pipeline.py` | JSONL ingestion + serialization |

### Technical decisions

- **float64** for statistical math (acceptable for pure TA per ecosystem rules)
- **No pandas / TA-Lib** — minimal dependency (NumPy only)
- **Explicit NaN** — downstream strategies can filter warmup
- **MACD:** the signal is calculated only over the finite portion of the MACD line

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

```bash
# All indicators
ta-indicators-from-scratch compute \
  --input samples/btcusdt_1m_candles.jsonl \
  --indicator all

# RSI only with custom period
ta-indicators-from-scratch compute \
  --input samples/btcusdt_1m_candles.jsonl \
  --indicator rsi \
  --rsi-period 14 \
  --output indicators.json
```

### Configurable parameters

| Flag | Indicator | Default |
|------|-----------|---------|
| `--sma-period` | SMA | 20 |
| `--ema-period` | EMA | 20 |
| `--rsi-period` | RSI | 14 |
| `--macd-fast/slow/signal` | MACD | 12 / 26 / 9 |
| `--bollinger-period/std` | Bollinger | 20 / 2.0 |

---

## Candle JSONL format

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

# Direct access to individual functions
rsi_values = rsi(series.close, period=14)
sma_values = sma(series.close, period=20)
```

---

## Development

```bash
pytest -q
ruff check src tests
mypy src
```

---

## Roadmap

- [ ] Additional indicators (ATR, Stochastic, VWAP)
- [ ] Parquet export of indicator series
- [ ] Direct pipeline from the lakehouse's DuckDB

---

## License

MIT
