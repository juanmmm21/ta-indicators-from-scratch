from __future__ import annotations

import argparse
import json
import logging

from ta_indicators_from_scratch.models import IndicatorConfig
from ta_indicators_from_scratch.pipeline import run_compute


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Indicadores técnicos vectorizados implementados desde cero con NumPy.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    compute = subparsers.add_parser("compute", help="Calcula indicadores sobre velas JSONL.")
    compute.add_argument("--input", required=True, help="Archivo JSON Lines con velas OHLCV.")
    compute.add_argument(
        "--indicator",
        default="all",
        choices=["all", "sma", "ema", "rsi", "macd", "bollinger"],
    )
    compute.add_argument("--sma-period", type=int, default=20)
    compute.add_argument("--ema-period", type=int, default=20)
    compute.add_argument("--rsi-period", type=int, default=14)
    compute.add_argument("--macd-fast", type=int, default=12)
    compute.add_argument("--macd-slow", type=int, default=26)
    compute.add_argument("--macd-signal", type=int, default=9)
    compute.add_argument("--bollinger-period", type=int, default=20)
    compute.add_argument("--bollinger-std", type=float, default=2.0)
    compute.add_argument("--output", default=None, help="Archivo JSON de salida opcional.")

    return parser


def main() -> None:
    args = build_parser().parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    if args.command == "compute":
        config = IndicatorConfig(
            sma_period=args.sma_period,
            ema_period=args.ema_period,
            rsi_period=args.rsi_period,
            macd_fast=args.macd_fast,
            macd_slow=args.macd_slow,
            macd_signal=args.macd_signal,
            bollinger_period=args.bollinger_period,
            bollinger_std=args.bollinger_std,
        )
        payload = run_compute(args.input, args.indicator, config)
        rendered = json.dumps(payload, indent=2)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as handle:
                handle.write(rendered)
                handle.write("\n")
            logging.getLogger(__name__).info("wrote indicator output to %s", args.output)
            return

        print(rendered)
        return

    raise RuntimeError(f"unsupported command: {args.command}")


if __name__ == "__main__":
    main()
