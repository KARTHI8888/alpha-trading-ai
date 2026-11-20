"""Signal accuracy and out-of-sample validation for ALPHA TRADING AI."""

from __future__ import annotations

from typing import Any

from backend.backtest import (
    MIN_CANDLES,
    TARGET_R_MULTIPLES,
    run_backtest,
    validate_candles,
)


def split_candles(
    candles: list[dict[str, Any]],
    train_ratio: float = 0.70,
) -> dict[str, Any]:
    """Split chronological candles into training and untouched test periods."""
    validate_candles(candles)

    if not 0.50 <= train_ratio <= 0.90:
        raise ValueError("train_ratio must be between 0.50 and 0.90.")

    split_index = int(len(candles) * train_ratio)

    if split_index < MIN_CANDLES or len(candles) - split_index < MIN_CANDLES:
        raise ValueError(
            "Not enough candles for both training and out-of-sample periods."
        )

    return {
        "train": candles[:split_index],
        "test": candles[split_index:],
        "split_index": split_index,
        "train_candles": split_index,
        "test_candles": len(candles) - split_index,
        "train_ratio_percent": round(train_ratio * 100, 2),
        "test_ratio_percent": round((1 - train_ratio) * 100, 2),
    }


def _accuracy_summary(trades: list[dict[str, Any]]) -> dict[str, Any]:
    """Summarize resolved and unresolved trade outcomes without guessing."""
    targets = [trade for trade in trades if trade["outcome"] == "TARGET"]
    losses = [trade for trade in trades if trade["outcome"] == "SL"]
    opened = [trade for trade in trades if trade["outcome"] == "OPEN"]

    resolved = len(targets) + len(losses)

    return {
        "target_wins": len(targets),
        "stop_losses": len(losses),
        "open_trades": len(opened),
        "resolved_trades": resolved,
        "total_trades": len(trades),
        "win_rate_percent": (
            round(len(targets) / resolved * 100, 2)
            if resolved
            else None
        ),
        "sample_warning": (
            "Insufficient sample: at least 100 resolved trades are recommended."
            if resolved < 100
            else None
        ),
    }


def validate_backtest(
    candles: list[dict[str, Any]],
    train_ratio: float = 0.70,
    spread_price: float = 0.0,
    slippage_per_side: float = 0.0,
    price_basis: str | None = None,
) -> dict[str, Any]:
    """Run separate in-sample and out-of-sample backtests."""
    split = split_candles(candles, train_ratio)

    common_costs = {
        "spread_price": spread_price,
        "slippage_per_side": slippage_per_side,
        "price_basis": price_basis,
    }

    training = run_backtest(split["train"], **common_costs)
    out_of_sample = run_backtest(
        candles,
        signal_start_index=split["split_index"],
        **common_costs,
    )

    scenarios = {}

    for target_number in TARGET_R_MULTIPLES:
        key = f"target{target_number}"

        train_result = training["scenarios"][key]
        test_result = out_of_sample["scenarios"][key]

        scenarios[key] = {
            "in_sample": {
                "metrics": train_result["metrics"],
                "accuracy": _accuracy_summary(train_result["trades"]),
            },
            "out_of_sample": {
                "metrics": test_result["metrics"],
                "accuracy": _accuracy_summary(test_result["trades"]),
            },
        }

    return {
        "status": "EXPERIMENTAL_VALIDATION",
        "candles_tested": len(candles),
        "split": {
            "train_candles": split["train_candles"],
            "test_candles": split["test_candles"],
            "train_ratio_percent": split["train_ratio_percent"],
            "test_ratio_percent": split["test_ratio_percent"],
        },
        "scenarios": scenarios,
        "limitations": [
            "Historical results do not guarantee future performance.",
            "Open trades are excluded from resolved-trade win rate.",
            "Out-of-sample results are not a guarantee of live accuracy.",
            "Each target is evaluated as a separate full-position exit.",
            "Spread and slippage are included only when configured.",
            "Commission is excluded.",
        ],
    }
