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


def atr(candles: list[dict], period: int = 14) -> Optional[float]:
    """Calculate Wilder's ATR from OHLC candles."""
    if len(candles) <= period:
        return None
    true_ranges = []
    for i in range(1, len(candles)):
        high = float(candles[i]["high"])
        low = float(candles[i]["low"])
        previous_close = float(candles[i - 1]["close"])
        true_ranges.append(max(high - low, abs(high - previous_close), abs(low - previous_close)))
    current = sum(true_ranges[:period]) / period
    for value in true_ranges[period:]:
        current = ((current * (period - 1)) + value) / period
    return round(current, 4)


def calculate_market_levels(candles: list[dict]) -> dict:
    """Return ATR and recent support/resistance reference levels."""
    if len(candles) < 20:
        raise ValueError("At least 20 candles are required.")
    recent = candles[-20:]
    return {
        "atr14": atr(candles),
        "support": round(min(float(c["low"]) for c in recent), 4),
        "resistance": round(max(float(c["high"]) for c in recent), 4),
    }


def analyze_candles(candles: list[dict]) -> dict:
    """Experimental rule-based analysis; not a guaranteed trading signal."""
    if len(candles) < 35:
        raise ValueError("At least 35 candles are required.")

    values = calculate_indicators(candles)
    levels = calculate_market_levels(candles)
    supertrend = calculate_supertrend(candles, period=10, multiplier=3.0)
    entry = float(candles[-1]["close"])
    atr_value = levels["atr14"]

    result = {
        "signal": "WAIT",
        "entry": None,
        "stop": None,
        "target1": None,
        "target2": None,
        "target3": None,
        "indicators": values,
        "levels": levels,
        "supertrend": supertrend,
        "message": "Conditions are not sufficiently aligned. WAIT.",
    }

    required = [
        values["ema9"], values["ema21"], values["rsi14"],
        values["macd"], values["macd_signal"], values["vwap"], atr_value,
    ]
    if any(value is None for value in required) or atr_value <= 0:
        return result

    buy = (
        values["ema9"] > values["ema21"]
        and 52 <= values["rsi14"] <= 68
        and values["macd"] > values["macd_signal"]
        and entry > values["vwap"]
    )
    sell = (
        values["ema9"] < values["ema21"]
        and 32 <= values["rsi14"] <= 48
        and values["macd"] < values["macd_signal"]
        and entry < values["vwap"]
    )

    if not (buy or sell):
        return result

    risk = atr_value * 1.5
    direction = 1 if buy else -1
    result.update({
        "signal": "BUY" if buy else "SELL",
        "entry": round(entry, 4),
        "stop": round(entry - direction * risk, 4),
        "target1": round(entry + direction * risk, 4),
        "target2": round(entry + direction * risk * 2, 4),
        "target3": round(entry + direction * risk * 3, 4),
        "message": "Experimental rule-based setup. Verify independently; not financial advice.",
    })
    return result


def calculate_supertrend(
    candles: list[dict],
    period: int = 10,
    multiplier: float = 3.0,
) -> dict:
    """Calculate Supertrend using Wilder ATR."""
    if len(candles) < period + 2:
        return {"value": None, "trend": "WAIT"}

    true_ranges = []
    for i in range(1, len(candles)):
        high = float(candles[i]["high"])
        low = float(candles[i]["low"])
        previous_close = float(candles[i - 1]["close"])
        true_ranges.append(
            max(high - low, abs(high - previous_close), abs(low - previous_close))
        )

    atr_values = [None] * len(candles)
    current_atr = sum(true_ranges[:period]) / period
    atr_values[period] = current_atr

    for i in range(period + 1, len(candles)):
        current_atr = (
            current_atr * (period - 1) + true_ranges[i - 1]
        ) / period
        atr_values[i] = current_atr

    final_upper = None
    final_lower = None
    trend = 1
    supertrend_value = None

    for i in range(period, len(candles)):
        atr_value = atr_values[i]
        midpoint = (
            float(candles[i]["high"]) + float(candles[i]["low"])
        ) / 2
        basic_upper = midpoint + multiplier * atr_value
        basic_lower = midpoint - multiplier * atr_value
        close = float(candles[i]["close"])

        if final_upper is None:
            final_upper = basic_upper
            final_lower = basic_lower
        else:
            previous_close = float(candles[i - 1]["close"])
            final_upper = (
                basic_upper if basic_upper < final_upper or previous_close > final_upper
                else final_upper
            )
            final_lower = (
                basic_lower if basic_lower > final_lower or previous_close < final_lower
                else final_lower
            )

        if trend == 1 and close < final_lower:
            trend = -1
        elif trend == -1 and close > final_upper:
            trend = 1

        supertrend_value = final_lower if trend == 1 else final_upper

    return {
        "value": round(supertrend_value, 4) if supertrend_value is not None else None,
        "trend": "BULLISH" if trend == 1 else "BEARISH",
        "atr_period": period,
        "multiplier": multiplier,
    }


def calculate_orb(
    candles: list[dict],
    opening_range_minutes: int = 15,
    candle_interval_minutes: int = 5,
) -> dict:
    """Calculate ORB from explicitly supplied opening-session candles."""
    required = opening_range_minutes // candle_interval_minutes

    if required < 1 or opening_range_minutes % candle_interval_minutes != 0:
        raise ValueError("Opening range must be divisible by candle interval.")

    if len(candles) < required:
        return {
            "status": "NOT_AVAILABLE",
            "high": None,
            "low": None,
            "breakout": "WAIT",
        }

    opening = candles[:required]
    orb_high = max(float(c["high"]) for c in opening)
    orb_low = min(float(c["low"]) for c in opening)
    latest_close = float(candles[-1]["close"])

    breakout = (
        "BULLISH_BREAKOUT" if latest_close > orb_high
        else "BEARISH_BREAKDOWN" if latest_close < orb_low
        else "WAIT"
    )

    return {
        "status": "CALCULATED",
        "high": round(orb_high, 4),
        "low": round(orb_low, 4),
        "breakout": breakout,
        "opening_range_minutes": opening_range_minutes,
    }


def calculate_cpr(
    previous_high: float,
    previous_low: float,
    previous_close: float,
) -> dict:
    """Calculate CPR from the previous completed trading day's OHLC."""
    high = float(previous_high)
    low = float(previous_low)
    close = float(previous_close)

    if low <= 0 or high < low or not low <= close <= high:
        raise ValueError("Invalid previous-day OHLC values.")

    pivot = (high + low + close) / 3
    bc = (high + low) / 2
    tc = (2 * pivot) - bc

    return {
        "pivot": round(pivot, 4),
        "tc": round(max(tc, bc), 4),
        "bc": round(min(tc, bc), 4),
        "status": "CALCULATED",
    }
