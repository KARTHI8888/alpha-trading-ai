import pytest

from backend.backtest import (
    validate_candles,
    calculate_execution_prices,
    calculate_net_pnl,
)


def test_validate_candles_accepts_valid_data():
    candles = [
        {
            "open": 2000.0,
            "high": 2002.0,
            "low": 1999.0,
            "close": 2001.0,
            "volume": 100.0,
        }
        for _ in range(35)
    ]

    validate_candles(candles)


@pytest.mark.parametrize("signal", ["BUY", "SELL"])
def test_spread_and_slippage_adjust_execution_prices(signal):
    entry, exit_price = calculate_execution_prices(
        signal=signal,
        entry=2000.0,
        exit_price=2002.0,
        spread_price=0.26,
        slippage_per_side=0.05,
    )

    if signal == "BUY":
        assert entry == pytest.approx(2000.18)
        assert exit_price == pytest.approx(2001.82)
    else:
        assert entry == pytest.approx(1999.82)
        assert exit_price == pytest.approx(2002.18)


def test_net_pnl_deducts_spread_and_slippage_only():
    result = calculate_net_pnl(
        signal="BUY",
        entry=2000.0,
        exit_price=2002.0,
        spread_price=0.26,
        slippage_per_side=0.05,
    )

    assert result["gross_pnl"] == pytest.approx(2.0)
    assert result["spread_cost"] == pytest.approx(0.26)
    assert result["slippage_cost"] == pytest.approx(0.10)
    assert result["net_pnl"] == pytest.approx(1.64)


def test_calculate_net_pnl_for_sell_trade():
    result = calculate_net_pnl(
        signal="SELL",
        entry=2000.0,
        exit_price=1998.0,
        spread_price=0.26,
        slippage_per_side=0.05,
    )

    assert result["gross_pnl"] == pytest.approx(2.0)
    assert result["spread_cost"] == pytest.approx(0.26)
    assert result["slippage_cost"] == pytest.approx(0.10)
    assert result["net_pnl"] == pytest.approx(1.64)


def test_calculate_net_pnl_rejects_negative_costs():
    with pytest.raises(ValueError):
        calculate_net_pnl(
            signal="BUY",
            entry=2000.0,
            exit_price=2002.0,
            spread_price=-0.26,
        )


def test_calculate_net_pnl_rejects_invalid_signal():
    with pytest.raises(ValueError):
        calculate_net_pnl(
            signal="HOLD",
            entry=2000.0,
            exit_price=2002.0,
        )


def test_run_backtest_applies_execution_costs(monkeypatch):
    from backend import backtest

    candles = [
        {
            "open": 2000.0,
            "high": 2000.5,
            "low": 1999.5,
            "close": 2000.0,
            "volume": 100.0,
        }
        for _ in range(35)
    ]

    candles.append({
        "open": 2000.0,
        "high": 2001.1,
        "low": 1999.5,
        "close": 2001.0,
        "volume": 120.0,
    })

    def fake_analyze_candles(history):
        return {
            "signal": "BUY",
            "levels": {"atr14": 1.0},
        }

    monkeypatch.setattr(
        backtest,
        "analyze_candles",
        fake_analyze_candles,
    )

    report = backtest.run_backtest(
        candles,
        spread_price=0.26,
        slippage_per_side=0.05,
        price_basis="MID",
    )

    trade = report["scenarios"]["target1"]["trades"][0]

    assert trade["outcome"] == "TARGET"
    assert trade["gross_pnl"] == pytest.approx(1.0)
    assert trade["spread_cost"] == pytest.approx(0.26)
    assert trade["slippage_cost"] == pytest.approx(0.10)
    assert trade["net_pnl"] == pytest.approx(0.64)


def test_run_backtest_rejects_costs_without_mid_price_basis():
    from backend.backtest import run_backtest

    candles = [
        {
            "open": 2000.0,
            "high": 2002.0,
            "low": 1999.0,
            "close": 2001.0,
            "volume": 100.0,
        }
        for _ in range(35)
    ]

    with pytest.raises(ValueError, match="price_basis='MID'"):
        run_backtest(candles, spread_price=0.26)


def test_run_backtest_costs_disabled_by_default():
    from backend.backtest import run_backtest

    candles = [
        {
            "open": 2000.0,
            "high": 2002.0,
            "low": 1999.0,
            "close": 2001.0,
            "volume": 100.0,
        }
        for _ in range(35)
    ]

    report = run_backtest(candles)

    assert report["methodology"]["costs"]["status"] == "DISABLED"
    assert report["methodology"]["costs"]["price_basis"] == "UNCONFIGURED"


def test_calculate_metrics_tracks_gross_and_net_results():
    from backend.backtest import calculate_metrics

    trades = [
        {"outcome": "TARGET", "pnl": 1.0, "net_pnl": 0.5, "atr": 1.0},
        {"outcome": "SL", "pnl": -1.0, "net_pnl": -1.5, "atr": 1.0},
        {"outcome": "TARGET", "pnl": 1.0, "net_pnl": 0.0, "atr": 1.0},
    ]

    metrics = calculate_metrics(trades)

    assert metrics["wins"] == 2
    assert metrics["losses"] == 1
    assert metrics["profit_factor"] == pytest.approx(2.0)

    assert metrics["net_wins"] == 1
    assert metrics["net_losses"] == 1
    assert metrics["net_breakeven_trades"] == 1
    assert metrics["net_win_rate_percent"] == pytest.approx(33.33)
    assert metrics["net_profit_factor"] == pytest.approx(0.3333)
    assert metrics["net_profit_r"] == pytest.approx(-1.0)
    assert metrics["net_max_drawdown_r"] == pytest.approx(1.5)


def test_run_backtest_counts_signals_only_after_start_index(monkeypatch):
    from backend import backtest

    candles = [
        {
            "open": 2000.0,
            "high": 2000.5,
            "low": 1999.5,
            "close": 2000.0,
            "volume": 100.0,
        }
        for _ in range(40)
    ]

    monkeypatch.setattr(
        backtest,
        "analyze_candles",
        lambda history: {
            "signal": "BUY",
            "levels": {"atr14": 1.0},
        },
    )

    report = backtest.run_backtest(
        candles,
        signal_start_index=36,
    )

    counts = report["scenarios"]["target1"]["signal_counts"]
    assert counts["BUY"] == 3
    assert counts["SELL"] == 0


def test_run_backtest_rejects_invalid_signal_start_index():
    from backend.backtest import run_backtest

    candles = [
        {
            "open": 2000.0,
            "high": 2002.0,
            "low": 1999.0,
            "close": 2001.0,
            "volume": 100.0,
        }
        for _ in range(40)
    ]

    with pytest.raises(ValueError, match="signal_start_index"):
        run_backtest(candles, signal_start_index=39)



def test_simulate_trade_records_exit_timestamp_and_reason():
    from backend.backtest import simulate_trade

    candles = [
        {
            "openTime": "2026-11-21T09:00:00Z",
            "open": 2000.0,
            "high": 2001.5,
            "low": 1999.5,
            "close": 2001.0,
            "volume": 100.0,
        }
    ]

    result = simulate_trade(candles, 0, "BUY", 2000.0, 1.0)

    assert result["target1"]["outcome"] == "TARGET"
    assert result["target1"]["exit_time"] == "2026-11-21T09:00:00Z"
    assert result["target1"]["exit_reason"] == "TARGET"


def test_simulate_trade_records_open_exit_timestamp():
    from backend.backtest import simulate_trade

    candles = [
        {
            "openTime": "2026-11-21T09:00:00Z",
            "open": 2000.0,
            "high": 2000.5,
            "low": 1999.5,
            "close": 2000.25,
            "volume": 100.0,
        }
    ]

    result = simulate_trade(candles, 0, "BUY", 2000.0, 1.0)

    assert result["target1"]["outcome"] == "OPEN"
    assert result["target1"]["exit_time"] == "2026-11-21T09:00:00Z"
    assert result["target1"]["exit_reason"] == "OPEN"


def test_candle_data_hash_is_deterministic():
    from backend.run_backtest import calculate_candle_data_hash

    candles = [
        {
            "openTime": "2026-11-21T09:00:00Z",
            "open": 2000.0,
            "high": 2002.0,
            "low": 1999.0,
            "close": 2001.0,
            "volume": 100.0,
        }
    ]

    first_hash = calculate_candle_data_hash(candles)
    second_hash = calculate_candle_data_hash(candles)

    assert len(first_hash) == 64
    assert first_hash == second_hash

    changed = [dict(candles[0], close=2001.5)]
    assert calculate_candle_data_hash(changed) != first_hash
