import pytest
from backend.indicators import (
    ema, dema, rsi, bollinger_bands,
    calculate_indicators, atr,
    calculate_market_levels, calculate_supertrend,
    analyze_candles,
)

def make_candles(count=50):
    candles = []
    for i in range(count):
        close = 2000 + i * 0.4
        candles.append({
            "open": close - 0.2,
            "high": close + 0.5,
            "low": close - 0.5,
            "close": close,
            "volume": 100 + i,
        })
    return candles

def test_ema():
    result = ema([1, 2, 3, 4, 5], 3)
    assert result[:2] == [None, None]
    assert result[2] == 2

def test_dema():
    result = dema(list(range(1, 20)), 3)
    assert result[-1] is not None

def test_rsi_uptrend():
    result = rsi(list(range(1, 20)), 14)
    assert result[-1] == 100

def test_rsi_flat_market():
    result = rsi([10] * 20, 14)
    assert result[-1] == 50

def test_bollinger_bands():
    result = bollinger_bands([10] * 20)
    assert result["upper"] == 10
    assert result["middle"] == 10
    assert result["lower"] == 10

def test_bollinger_insufficient_data():
    result = bollinger_bands([10] * 10)
    assert result["middle"] is None

def test_calculate_indicators():
    result = calculate_indicators(make_candles())
    for key in (
        "ema9", "ema21", "dema9", "rsi14",
        "macd", "macd_signal", "vwap",
        "bb_upper", "bb_middle", "bb_lower",
    ):
        assert result[key] is not None

def test_atr():
    assert atr(make_candles()) == 1.0

def test_market_levels():
    result = calculate_market_levels(make_candles())
    assert result["atr14"] == 1.0
    assert result["support"] < result["resistance"]

def test_supertrend():
    result = calculate_supertrend(make_candles())
    assert result["trend"] == "BULLISH"
    assert result["value"] is not None

def test_analyze_candles_wait():
    result = analyze_candles(make_candles())
    assert result["signal"] == "WAIT"
    assert result["entry"] is None
    assert result["stop"] is None

def test_insufficient_candles():
    with pytest.raises(ValueError):
        analyze_candles(make_candles(20))


def make_signal_candles(drift, volume=100.0):
    import math

    candles = []
    for i in range(100):
        close = 2000 + drift * i + 1.5 * math.sin(i * 0.55)
        candles.append({
            "open": close - 0.1,
            "high": close + 0.5,
            "low": close - 0.5,
            "close": close,
            "volume": volume,
        })
    candles[-1]["volume"] = volume * 1.5
    return candles


def test_analyze_candles_generates_buy_with_atr_levels():
    result = analyze_candles(make_signal_candles(0.18))

    assert result["signal"] == "BUY"
    assert result["entry"] is not None
    assert result["stop"] < result["entry"]
    assert result["target1"] > result["entry"]
    assert result["target1"] < result["target2"] < result["target3"]
    assert result["volume_confirmation"] is True


def test_analyze_candles_generates_sell_with_atr_levels():
    result = analyze_candles(make_signal_candles(-0.04))

    assert result["signal"] == "SELL"
    assert result["entry"] is not None
    assert result["stop"] > result["entry"]
    assert result["target1"] < result["entry"]
    assert result["target1"] > result["target2"] > result["target3"]
    assert result["volume_confirmation"] is True


def test_analyze_candles_waits_when_rsi_is_outside_sell_range():
    result = analyze_candles(make_signal_candles(-0.12))

    assert result["indicators"]["rsi14"] < 32
    assert result["signal"] == "WAIT"
    assert result["entry"] is None


def test_analyze_candles_waits_without_volume_confirmation():
    candles = make_signal_candles(0.18)
    candles[-1]["volume"] = 0

    result = analyze_candles(candles)

    assert result["volume_confirmation"] is False
    assert result["signal"] == "WAIT"
    assert result["entry"] is None
