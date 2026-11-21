"""Historical backtesting for the ALPHA TRADING AI rule-based signal engine."""

from __future__ import annotations

import math

from typing import Any

from backend.indicators import analyze_candles


MIN_CANDLES = 35
LOOKBACK_CANDLES = 50
TARGET_R_MULTIPLES = (1, 2, 3)


def validate_candles(candles: list[dict[str, Any]]) -> None:
    """Validate chronological OHLCV candle data."""
    if len(candles) < MIN_CANDLES:
        raise ValueError(f"At least {MIN_CANDLES} candles are required.")

    previous_time = None

    for index, candle in enumerate(candles):
        for key in ("open", "high", "low", "close", "volume"):
            if key not in candle:
                raise ValueError(f"Candle {index} is missing {key}.")

        open_price = float(candle["open"])
        high = float(candle["high"])
        low = float(candle["low"])
        close = float(candle["close"])
        volume = float(candle["volume"])

        if not all(map(__import__("math").isfinite, (
            open_price, high, low, close, volume
        ))):
            raise ValueError(f"Candle {index} contains non-finite values.")

        if low > high or low > min(open_price, close) or high < max(open_price, close):
            raise ValueError(f"Candle {index} has invalid OHLC prices.")

        if volume < 0:
            raise ValueError(f"Candle {index} has negative volume.")

        candle_time = candle.get("openTime")
        if candle_time is not None:
            if previous_time is not None and candle_time <= previous_time:
                raise ValueError("Candles must be in strictly increasing time order.")
            previous_time = candle_time



def calculate_execution_prices(
    signal: str,
    entry: float,
    exit_price: float,
    spread_price: float = 0.0,
    slippage_per_side: float = 0.0,
) -> tuple[float, float]:
    """Calculate adverse entry and exit prices using a MID-price input."""
    if signal not in ("BUY", "SELL"):
        raise ValueError("Signal must be BUY or SELL.")

    values = (entry, exit_price, spread_price, slippage_per_side)
    if not all(math.isfinite(float(value)) for value in values):
        raise ValueError("Execution prices and costs must be finite.")

    if entry <= 0 or exit_price <= 0:
        raise ValueError("Entry and exit prices must be positive.")

    if spread_price < 0 or slippage_per_side < 0:
        raise ValueError("Spread and slippage cannot be negative.")

    half_spread = spread_price / 2
    direction = 1 if signal == "BUY" else -1

    adjusted_entry = entry + direction * (half_spread + slippage_per_side)
    adjusted_exit = exit_price - direction * (half_spread + slippage_per_side)

    return adjusted_entry, adjusted_exit


def calculate_net_pnl(
    signal: str,
    entry: float,
    exit_price: float,
    spread_price: float = 0.0,
    slippage_per_side: float = 0.0,
) -> dict[str, float]:
    """Calculate net PnL using adverse execution prices from MID prices."""
    if signal not in ("BUY", "SELL"):
        raise ValueError("Signal must be BUY or SELL.")

    values = (
        entry,
        exit_price,
        spread_price,
        slippage_per_side,
    )
    if not all(math.isfinite(float(value)) for value in values):
        raise ValueError("Prices and costs must be finite.")

    if entry <= 0 or exit_price <= 0:
        raise ValueError("Prices must be positive.")

    if any(value < 0 for value in values[2:]):
        raise ValueError("Execution costs cannot be negative.")

    adjusted_entry, adjusted_exit = calculate_execution_prices(
        signal=signal,
        entry=entry,
        exit_price=exit_price,
        spread_price=spread_price,
        slippage_per_side=slippage_per_side,
    )

    direction = 1 if signal == "BUY" else -1
    gross_pnl = direction * (exit_price - entry)
    execution_pnl = direction * (adjusted_exit - adjusted_entry)

    spread_cost = spread_price
    slippage_cost = slippage_per_side * 2
    net_pnl = execution_pnl

    return {
        "gross_pnl": round(gross_pnl, 6),
        "adjusted_entry": round(adjusted_entry, 6),
        "adjusted_exit": round(adjusted_exit, 6),
        "execution_pnl": round(execution_pnl, 6),
        "spread_cost": round(spread_cost, 6),
        "slippage_cost": round(slippage_cost, 6),
        "net_pnl": round(net_pnl, 6),
    }

def build_trade_levels(
    signal: str,
    entry: float,
    atr_value: float,
) -> dict[str, float]:
    """Build stop-loss and three target levels from the signal ATR."""
    if signal not in ("BUY", "SELL"):
        raise ValueError("Signal must be BUY or SELL.")

    if not all(map(__import__("math").isfinite, (entry, atr_value))):
        raise ValueError("Entry and ATR must be finite numbers.")

    if entry <= 0 or atr_value <= 0:
        raise ValueError("Entry and ATR must be positive.")

    direction = 1 if signal == "BUY" else -1

    return {
        "entry": entry,
        "stop": entry - direction * atr_value,
        "target1": entry + direction * atr_value,
        "target2": entry + direction * 2 * atr_value,
        "target3": entry + direction * 3 * atr_value,
    }


def simulate_trade(
    candles: list[dict[str, Any]],
    entry_index: int,
    signal: str,
    entry: float,
    atr_value: float,
) -> dict[str, dict[str, Any]]:
    """Simulate separate full-position exits at TP1, TP2 and TP3."""
    if signal not in ("BUY", "SELL"):
        raise ValueError("Signal must be BUY or SELL.")

    if entry_index < 0 or entry_index >= len(candles):
        raise ValueError("Invalid entry candle index.")

    levels = build_trade_levels(signal, entry, atr_value)
    is_buy = signal == "BUY"
    outcomes = {}

    for target_number in TARGET_R_MULTIPLES:
        target_key = f"target{target_number}"
        target_price = levels[target_key]
        outcome = "OPEN"
        exit_price = None
        exit_index = None

        for index in range(entry_index, len(candles)):
            candle = candles[index]
            high = float(candle["high"])
            low = float(candle["low"])

            if is_buy:
                stop_hit = low <= levels["stop"]
                target_hit = high >= target_price
            else:
                stop_hit = high >= levels["stop"]
                target_hit = low <= target_price

            # Conservative rule: assume SL first if both are touched.
            if stop_hit:
                outcome = "SL"
                exit_price = levels["stop"]
                exit_index = index
                break

            if target_hit:
                outcome = "TARGET"
                exit_price = target_price
                exit_index = index
                break

        if outcome == "OPEN":
            exit_index = len(candles) - 1
            exit_price = float(candles[exit_index]["close"])

        direction = 1 if is_buy else -1
        pnl = direction * (exit_price - entry)

        outcomes[target_key] = {
            "outcome": outcome,
            "entry": round(entry, 6),
            "exit": round(exit_price, 6),
            "pnl": round(pnl, 6),
            "exit_index": exit_index,
            "exit_time": candles[exit_index].get("openTime"),
            "exit_reason": outcome,
            "target_price": round(target_price, 6),
            "stop_price": round(levels["stop"], 6),
        }

    return outcomes



def calculate_metrics(trades: list[dict[str, Any]]) -> dict[str, Any]:
    """Calculate gross and net performance in normalized R units."""
    closed = [t for t in trades if t["outcome"] in ("TARGET", "SL")]
    gross_wins = [t for t in closed if t["pnl"] > 0]
    gross_losses = [t for t in closed if t["pnl"] < 0]
    opened = [t for t in trades if t["outcome"] == "OPEN"]

    gross_profit_r = sum(t["pnl"] / t["atr"] for t in gross_wins)
    gross_loss_r = abs(sum(t["pnl"] / t["atr"] for t in gross_losses))
    gross_equity = 0.0
    gross_peak = 0.0
    gross_drawdown = 0.0

    for trade in closed:
        gross_equity += trade["pnl"] / trade["atr"]
        gross_peak = max(gross_peak, gross_equity)
        gross_drawdown = max(gross_drawdown, gross_peak - gross_equity)

    gross_pf = round(gross_profit_r / gross_loss_r, 4) if gross_loss_r else None

    net_values = [
        (float(t.get("net_pnl", t["pnl"])), float(t["atr"]))
        for t in closed
    ]
    net_wins = [(pnl, atr) for pnl, atr in net_values if pnl > 0]
    net_losses = [(pnl, atr) for pnl, atr in net_values if pnl < 0]
    net_profit_r = sum(pnl / atr for pnl, atr in net_wins)
    net_loss_r = abs(sum(pnl / atr for pnl, atr in net_losses))
    net_equity = 0.0
    net_peak = 0.0
    net_drawdown = 0.0

    for pnl, atr in net_values:
        net_equity += pnl / atr
        net_peak = max(net_peak, net_equity)
        net_drawdown = max(net_drawdown, net_peak - net_equity)

    net_pf = round(net_profit_r / net_loss_r, 4) if net_loss_r else None

    return {
        "closed_trades": len(closed),
        "wins": len(gross_wins),
        "losses": len(gross_losses),
        "open_trades": len(opened),
        "target_hits": sum(1 for t in closed if t["outcome"] == "TARGET"),
        "stop_loss_hits": sum(1 for t in closed if t["outcome"] == "SL"),
        "win_rate_percent": round(len(gross_wins) / len(closed) * 100, 2) if closed else None,
        "profit_factor": gross_pf,
        "profit_factor_note": (
            "No losing closed trades; profit factor is unbounded."
            if gross_profit_r > 0 and gross_loss_r == 0
            else "No closed losing trades or no closed trades."
            if gross_loss_r == 0
            else None
        ),
        "gross_profit_r": round(gross_profit_r, 4),
        "gross_loss_r": round(gross_loss_r, 4),
        "net_profit_r": round(net_profit_r - net_loss_r, 4),
        "max_drawdown_r": round(gross_drawdown, 4),
        "drawdown_method": "Closed-trade realized equity in R; open trades excluded.",
        "net_wins": len(net_wins),
        "net_losses": len(net_losses),
        "net_breakeven_trades": len(closed) - len(net_wins) - len(net_losses),
        "net_win_rate_percent": round(len(net_wins) / len(closed) * 100, 2) if closed else None,
        "net_profit_factor": net_pf,
        "net_profit_factor_note": (
            "No net losing closed trades; profit factor is unbounded."
            if net_profit_r > 0 and net_loss_r == 0
            else "No net losing closed trades or no closed trades."
            if net_loss_r == 0
            else None
        ),
        "net_gross_profit_r": round(net_profit_r, 4),
        "net_gross_loss_r": round(net_loss_r, 4),
        "net_max_drawdown_r": round(net_drawdown, 4),
    }

def run_backtest(
    candles: list[dict[str, Any]],
    spread_price: float = 0.0,
    slippage_per_side: float = 0.0,
    price_basis: str | None = None,
    signal_start_index: int | None = None,
) -> dict[str, Any]:
    """Run TP scenarios with optional costs, requiring explicit MID basis."""
    costs = (spread_price, slippage_per_side)
    if not all(math.isfinite(float(value)) for value in costs):
        raise ValueError("Execution costs must be finite.")
    if any(value < 0 for value in costs):
        raise ValueError("Execution costs cannot be negative.")
    if any(value > 0 for value in costs) and price_basis != "MID":
        raise ValueError("Non-zero costs currently require price_basis='MID'.")

    validate_candles(candles)

    using_default_start = signal_start_index is None

    if using_default_start:
        signal_start_index = MIN_CANDLES - 1

    if (
        not isinstance(signal_start_index, int)
        or isinstance(signal_start_index, bool)
        or signal_start_index < MIN_CANDLES - 1
        or (
            not using_default_start
            and signal_start_index >= len(candles) - 1
        )
    ):
        raise ValueError("signal_start_index is outside the valid signal range.")

    # Earlier candles provide indicator warm-up history.
    # Only signals from the requested evaluation period are counted.
    signal_history = []
    all_counts = {"BUY": 0, "SELL": 0, "WAIT": 0}

    for i in range(signal_start_index, len(candles) - 1):
        history = candles[max(0, i - LOOKBACK_CANDLES + 1):i + 1]

        try:
            result = analyze_candles(history)
        except ValueError:
            signal_history.append({
                "signal_index": i,
                "signal": "WAIT",
                "atr": None,
            })
            all_counts["WAIT"] += 1
            continue

        signal = result.get("signal", "WAIT")
        if signal not in all_counts:
            signal = "WAIT"

        all_counts[signal] += 1

        atr_value = result.get("levels", {}).get("atr14")
        if (
            not isinstance(atr_value, (int, float))
            or not math.isfinite(float(atr_value))
            or atr_value <= 0
        ):
            atr_value = None

        signal_history.append({
            "signal_index": i,
            "signal": signal,
            "atr": float(atr_value) if atr_value is not None else None,
        })

    scenarios = {}

    for target_number in TARGET_R_MULTIPLES:
        key = f"target{target_number}"
        trades = []
        next_index = MIN_CANDLES - 1

        for opportunity in signal_history:
            i = opportunity["signal_index"]

            if i < next_index:
                continue

            signal = opportunity["signal"]
            atr_value = opportunity["atr"]

            if signal == "WAIT" or atr_value is None:
                continue

            entry_index = i + 1
            entry = float(candles[entry_index]["open"])

            outcome = simulate_trade(
                candles, entry_index, signal, entry, atr_value
            )[key]

            cost_result = calculate_net_pnl(
                signal=signal,
                entry=outcome["entry"],
                exit_price=outcome["exit"],
                spread_price=spread_price,
                slippage_per_side=slippage_per_side,
            )

            trades.append({
                "signal": signal,
                "signal_index": i,
                "entry_index": entry_index,
                "signal_time": candles[i].get("openTime"),
                "entry_time": candles[entry_index].get("openTime"),
                "atr": round(atr_value, 6),
                "target": key,
                **outcome,
                **cost_result,
            })

            next_index = outcome["exit_index"] + 1

        scenarios[key] = {
            "trade_count": len(trades),
            "signal_counts": dict(all_counts),
            "metrics": calculate_metrics(trades),
            "trades": trades,
        }

    return {
        "candles_tested": len(candles),
        "scenarios": scenarios,
        "methodology": {
            "lookback_candles": LOOKBACK_CANDLES,
            "entry": "Next candle open",
            "stop_distance": "1 ATR",
            "targets": ["1 ATR", "2 ATR", "3 ATR"],
            "signal_counts": "All evaluated opportunities, including signals during open trades",
            "same_candle_rule": "Stop loss assumed first",
            "overlapping_trades": "Disabled independently per target",
            "costs": {
                "price_basis": price_basis or "UNCONFIGURED",
                "spread_price": spread_price,
                "slippage_per_side": slippage_per_side,
                "status": "CONFIGURED" if any(value > 0 for value in costs) else "DISABLED",
                "execution_model": "MID_OHLC_WITH_ADVERSE_ENTRY_EXIT_ADJUSTMENTS",
                "trigger_model": "MID_OHLC_STOP_TARGET_TRIGGERS",
                "limitations": (
                    "Historical Bid/Ask OHLC is unavailable. Stop and target triggers "
                    "use MID OHLC; spread and slippage adjust execution prices."
                ),
            },
        },
    }
