"""Multi-timeframe historical backtest runner."""

import json
import os
from urllib.request import Request, urlopen
from datetime import datetime, timezone
from pathlib import Path

from backend.backtest import run_backtest

SYMBOL = "XAUUSD"
INTERVALS = ("1h", "4h", "1d")
HISTORY_LIMIT = 1000

# Optional execution-cost assumptions (price units, not account currency).
SPREAD_PRICE = float(os.getenv("ALPHA_SPREAD_PRICE", "0"))
SLIPPAGE_PER_SIDE = float(os.getenv("ALPHA_SLIPPAGE_PER_SIDE", "0"))
COMMISSION_PRICE_EQUIVALENT = float(
    os.getenv("ALPHA_COMMISSION_PRICE_EQUIVALENT", "0")
)


def fetch_historical_candles(interval: str) -> list[dict]:
    url = (
        f"https://biquote.io/api/{SYMBOL}/ohlc"
        f"?interval={interval}&limit={HISTORY_LIMIT}"
    )
    request = Request(
        url,
        headers={"User-Agent": "ALPHA-TRADING-AI/1.0"},
    )

    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))

    bars = payload.get("bars", [])
    closed_bars = [
        bar for bar in bars if bar.get("isOpen") is False
    ]
    closed_bars.sort(key=lambda bar: bar["openTime"])

    candles = [
        {
            "openTime": bar["openTime"],
            "open": float(bar["open"]),
            "high": float(bar["high"]),
            "low": float(bar["low"]),
            "close": float(bar["close"]),
            "volume": float(
                bar.get("tickVolume", bar.get("volume", 0))
            ),
        }
        for bar in closed_bars
    ]

    if len(candles) < 35:
        raise ValueError(
            f"{interval}: Not enough closed candles: {len(candles)}"
        )

    return candles


def main():
    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)

    for interval in INTERVALS:
        print(f"\nFetching {SYMBOL} {interval} candles...")

        try:
            candles = fetch_historical_candles(interval)
            result = run_backtest(
                candles,
                spread_price=SPREAD_PRICE,
                slippage_per_side=SLIPPAGE_PER_SIDE,
                commission_price_equivalent=COMMISSION_PRICE_EQUIVALENT,
                price_basis="MID",
            )

            report = {
                "symbol": SYMBOL,
                "interval": interval,
                "data_source": "BiQuote",
                "first_candle": candles[0]["openTime"],
                "last_candle": candles[-1]["openTime"],
                "generated_at": datetime.now(timezone.utc).isoformat(),
                **result,
            }

            report_path = (
                report_dir / f"xauusd_{interval}_backtest.json"
            )
            report_path.write_text(
                json.dumps(report, indent=2)
            )

            print("Backtest completed.")
            print("Candles tested:", result["candles_tested"])

            for target, scenario in result["scenarios"].items():
                print(f"\n{target}")
                print("Trades:", scenario["trade_count"])
                print("Signals:", scenario["signal_counts"])
                print("Metrics:", scenario["metrics"])

            print("Report saved:", report_path)

        except Exception as exc:
            print(f"ERROR: {interval} backtest failed: {exc}")


if __name__ == "__main__":
    main()
