# ta-indicators-from-scratch

Librería de **análisis técnico vectorizado** que implementa indicadores clásicos desde cero con NumPy — sin TA-Lib, pandas-ta ni dependencias de terceros. Cuarto módulo del ecosistema [quant-core-infra](https://github.com/juanmmm21/quant-core-infra).

Repositorio: [github.com/juanmmm21/ta-indicators-from-scratch](https://github.com/juanmmm21/ta-indicators-from-scratch)

---

## Qué es y qué problema resuelve

Las librerías de indicadores (TA-Lib, etc.) son cajas negras: devuelven un número sin que el desarrollador entienda la matemática exacta. En un portafolio cuantitativo eso es un problema: no puedes auditar, optimizar ni explicar las señales.

Este proyecto implementa las fórmulas **explícitamente** con operaciones vectorizadas de NumPy:

- Sabes exactamente qué ocurre en cada ventana de warmup
- Puedes componer indicadores en pipelines propios
- El rendimiento se mantiene a nivel C gracias a la vectorización

Consume velas OHLCV de `market-data-lakehouse` y alimenta `alpha-signal-generator`.

---

## Rol en quant-core-infra

```text
market-data-lakehouse ──► velas OHLCV ──► ta-indicators-from-scratch ──► indicadores
                                                    │
                                          alpha-signal-generator
```

Traduce **precio histórico** en **features estadísticas** que las estrategias evalúan barra a barra.

---

## Indicadores soportados

| Indicador | Función | Parámetros por defecto | Fórmula clave |
|-----------|---------|------------------------|---------------|
| **SMA** | Media móvil simple | periodo `20` | Media aritmética de N cierres |
| **EMA** | Media móvil exponencial | periodo `20` | `α = 2/(N+1)`, semilla SMA |
| **RSI** | Índice de fuerza relativa | periodo `14` | Suavizado de Wilder sobre gains/losses |
| **MACD** | Convergencia/divergencia | `12 / 26 / 9` | EMA rápida − EMA lenta, señal EMA |
| **Bollinger** | Bandas de volatilidad | periodo `20`, σ `2.0` | SMA ± k·σ móvil |

Todos devuelven `NaN` durante la ventana de warmup hasta acumular suficientes velas.

---

## Cómo funciona

1. **Entrada:** arrays `float64` o JSONL con campos OHLCV.
2. **Contenedor:** `OhlcvSeries` valida longitudes y valores finitos.
3. **Cálculo:** cada indicador es una función pura `ndarray → ndarray`.
4. **Motor:** `TechnicalAnalysisEngine` orquesta todos los indicadores sobre la misma serie.
5. **Salida:** `IndicatorResult` con arrays alineados por índice de vela.
6. **CLI:** serializa a JSON con `null` donde hay `NaN`.

---

## Arquitectura

```text
OHLCV candles (JSONL / arrays)
        │
        ▼
OhlcvSeries
        │
        ▼
TechnicalAnalysisEngine
   ├─ sma / ema / rsi
   ├─ macd (línea, señal, histograma)
   └─ bollinger_bands (media, superior, inferior)
        │
        ▼
IndicatorResult
```

### Componentes

| Módulo | Responsabilidad |
|--------|----------------|
| `series.py` | Contenedor OHLCV y parsing de records |
| `indicators/sma.py` | SMA por convolución + std móvil |
| `indicators/ema.py` | EMA con semilla SMA |
| `indicators/rsi.py` | RSI Wilder |
| `indicators/macd.py` | Stack MACD completo |
| `indicators/bollinger.py` | Bandas alrededor de SMA |
| `engine.py` | Orquestación multi-indicador |
| `pipeline.py` | Ingesta JSONL + serialización |

### Decisiones técnicas

- **float64** para matemática estadística (aceptable para TA pura según reglas del ecosistema)
- **Sin pandas / TA-Lib** — dependencia mínima (solo NumPy)
- **NaN explícitos** — las estrategias downstream pueden filtrar warmup
- **MACD:** la señal se calcula solo sobre la porción finita de la línea MACD

---

## Requisitos

- Python **3.11+**

---

## Instalación

```bash
cd ta-indicators-from-scratch
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

---

## Uso CLI

```bash
# Todos los indicadores
ta-indicators-from-scratch compute \
  --input samples/btcusdt_1m_candles.jsonl \
  --indicator all

# Solo RSI con periodo custom
ta-indicators-from-scratch compute \
  --input samples/btcusdt_1m_candles.jsonl \
  --indicator rsi \
  --rsi-period 14 \
  --output indicators.json
```

### Parámetros configurables

| Flag | Indicador | Default |
|------|-----------|---------|
| `--sma-period` | SMA | 20 |
| `--ema-period` | EMA | 20 |
| `--rsi-period` | RSI | 14 |
| `--macd-fast/slow/signal` | MACD | 12 / 26 / 9 |
| `--bollinger-period/std` | Bollinger | 20 / 2.0 |

---

## Formato JSONL de velas

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

## Uso programático

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

# Acceso directo a funciones individuales
rsi_values = rsi(series.close, period=14)
sma_values = sma(series.close, period=20)
```

---

## Desarrollo

```bash
pytest -q
ruff check src tests
mypy src
```

---

## Roadmap

- [ ] Indicadores adicionales (ATR, Stochastic, VWAP)
- [ ] Export Parquet de series de indicadores
- [ ] Pipeline directo desde DuckDB del lakehouse

---

## Licencia

MIT
