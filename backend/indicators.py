"""Pure-Python technical indicators for ALPHA TRADING AI."""

from typing import Optional


def ema(values: list[float], period: int) -> list[Optional[float]]:
    result = [None] * len(values)
    if len(values) < period:
        return result

    current = sum(values[:period]) / period
    result[period - 1] = current
    multiplier = 2 / (period + 1)

    for i in range(period, len(values)):
        current = (values[i] - current) * multiplier + current
        result[i] = current

    return result


def rsi(values: list[float], period: int = 14) -> list[Optional[float]]:
    result = [None] * len(values)
    if len(values) <= period:
        return result

    changes = [values[i] - values[i - 1] for i in range(1, len(values))]
    gains = [max(change, 0) for change in changes]
    losses = [max(-change, 0) for change in changes]

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period

    def value(gain: float, loss: float) -> float:
        if gain == 0 and loss == 0:
            return 50.0
        if loss == 0:
            return 100.0
        return 100 - (100 / (1 + gain / loss))

    result[period] = value(avg_gain, avg_loss)

    for i in range(period + 1, len(values)):
        avg_gain = ((avg_gain * (period - 1)) + gains[i - 1]) / period
        avg_loss = ((avg_loss * (period - 1)) + losses[i - 1]) / period
        result[i] = value(avg_gain, avg_loss)

    return result


def calculate_indicators(candles: list[dict]) -> dict:
    """Calculate EMA 9/21, RSI 14, MACD and cumulative VWAP."""

    if len(candles) < 35:
        raise ValueError("At least 35 candles are required.")

    closes = [float(c["close"]) for c in candles]
    highs = [float(c["high"]) for c in candles]
    lows = [float(c["low"]) for c in candles]
    volumes = [float(c["volume"]) for c in candles]

    for i, candle in enumerate(candles):
        if min(closes[i], highs[i], lows[i]) <= 0 or volumes[i] < 0:
            raise ValueError("Prices must be positive and volume cannot be negative.")
        if highs[i] < max(candle["open"], closes[i], lows[i]):
            raise ValueError("Invalid candle high.")
        if lows[i] > min(candle["open"], closes[i], highs[i]):
            raise ValueError("Invalid candle low.")

    ema9 = ema(closes, 9)
    ema21 = ema(closes, 21)
    rsi14 = rsi(closes, 14)

    fast = ema(closes, 12)
    slow = ema(closes, 26)
    macd_line = [
        (fast[i] - slow[i]) if fast[i] is not None and slow[i] is not None else None
        for i in range(len(closes))
    ]

    valid_macd = [v for v in macd_line if v is not None]
    signal_values = ema(valid_macd, 9)
    macd_signal = [None] * len(closes)

    start = len(closes) - len(valid_macd)
    for i, value in enumerate(signal_values):
        macd_signal[start + i] = value

    cumulative_pv = 0.0
    cumulative_volume = 0.0
    vwap = None

    for candle in candles:
        typical_price = (
            float(candle["high"]) + float(candle["low"]) + float(candle["close"])
        ) / 3
        volume = float(candle["volume"])
        cumulative_pv += typical_price * volume
        cumulative_volume += volume

    if cumulative_volume > 0:
        vwap = cumulative_pv / cumulative_volume

    return {
        "ema9": round(ema9[-1], 4) if ema9[-1] is not None else None,
        "ema21": round(ema21[-1], 4) if ema21[-1] is not None else None,
        "rsi14": round(rsi14[-1], 2) if rsi14[-1] is not None else None,
        "macd": round(macd_line[-1], 4) if macd_line[-1] is not None else None,
        "macd_signal": round(macd_signal[-1], 4) if macd_signal[-1] is not None else None,
        "vwap": round(vwap, 4) if vwap is not None else None,
    }
