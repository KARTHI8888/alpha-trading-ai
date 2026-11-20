import pytest

from backend.validation import (
    split_candles,
    _accuracy_summary,
)


def make_candles(count):
    return [
        {
            "open": 2000.0,
            "high": 2002.0,
            "low": 1999.0,
            "close": 2001.0,
            "volume": 100.0,
        }
        for _ in range(count)
    ]


def test_split_candles_uses_chronological_70_30_split():
    candles = make_candles(120)
    result = split_candles(candles)

    assert result["train_candles"] == 84
    assert result["test_candles"] == 36
    assert result["train"] == candles[:84]
    assert result["test"] == candles[84:]


def test_split_candles_rejects_small_dataset():
    with pytest.raises(ValueError, match="Not enough candles"):
        split_candles(make_candles(60))


def test_split_candles_rejects_invalid_ratio():
    with pytest.raises(ValueError, match="train_ratio"):
        split_candles(make_candles(100), train_ratio=0.95)


def test_accuracy_summary_excludes_open_trades():
    trades = [
        {"outcome": "TARGET"},
        {"outcome": "TARGET"},
        {"outcome": "SL"},
        {"outcome": "OPEN"},
    ]

    result = _accuracy_summary(trades)

    assert result["target_wins"] == 2
    assert result["stop_losses"] == 1
    assert result["open_trades"] == 1
    assert result["resolved_trades"] == 3
    assert result["total_trades"] == 4
    assert result["win_rate_percent"] == pytest.approx(66.67)
    assert result["sample_warning"] is not None


def test_accuracy_summary_handles_no_resolved_trades():
    result = _accuracy_summary([{"outcome": "OPEN"}])

    assert result["win_rate_percent"] is None
    assert result["resolved_trades"] == 0


def test_accuracy_summary_removes_warning_at_100_resolved_trades():
    trades = [
        {"outcome": "TARGET"} for _ in range(60)
    ] + [
        {"outcome": "SL"} for _ in range(40)
    ]

    result = _accuracy_summary(trades)

    assert result["resolved_trades"] == 100
    assert result["win_rate_percent"] == 60.0
    assert result["sample_warning"] is None
