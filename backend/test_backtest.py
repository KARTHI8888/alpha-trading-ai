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


def test_net_pnl_deducts_commission():
    result = calculate_net_pnl(
        signal="BUY",
        entry=2000.0,
        exit_price=2002.0,
        spread_price=0.26,
        slippage_per_side=0.05,
        commission_price_equivalent=0.10,
    )

    assert result["gross_pnl"] == pytest.approx(2.0)
    assert result["spread_cost"] == pytest.approx(0.26)
    assert result["slippage_cost"] == pytest.approx(0.10)
    assert result["commission_cost"] == pytest.approx(0.10)
    assert result["net_pnl"] == pytest.approx(1.54)


def test_calculate_net_pnl_for_sell_trade():
    result = calculate_net_pnl(
        signal="SELL",
        entry=2000.0,
        exit_price=1998.0,
        spread_price=0.26,
        slippage_per_side=0.05,
        commission_price_equivalent=0.10,
    )

    assert result["gross_pnl"] == pytest.approx(2.0)
    assert result["spread_cost"] == pytest.approx(0.26)
    assert result["slippage_cost"] == pytest.approx(0.10)
    assert result["commission_cost"] == pytest.approx(0.10)
    assert result["net_pnl"] == pytest.approx(1.54)


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
        commission_price_equivalent=0.10,
        price_basis="MID",
    )

    trade = report["scenarios"]["target1"]["trades"][0]

    assert trade["outcome"] == "TARGET"
    assert trade["gross_pnl"] == pytest.approx(1.0)
    assert trade["spread_cost"] == pytest.approx(0.26)
    assert trade["slippage_cost"] == pytest.approx(0.10)
    assert trade["commission_cost"] == pytest.approx(0.10)
    assert trade["net_pnl"] == pytest.approx(0.54)


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
