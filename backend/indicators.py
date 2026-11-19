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



def dema(values: list[float], period: int = 9) -> list[Optional[float]]:
    """Calculate Double Exponential Moving Average."""
    first = ema(values, period)
    valid_start = next((i for i, value in enumerate(first) if value is not None), None)
    result = [None] * len(values)
    if valid_start is None:
        return result

    second = ema([float(v) for v in first[valid_start:]], period)
    for i, value in enumerate(second):
        if value is not None:
            result[valid_start + i] = 2 * first[valid_start + i] - value
    return result


def bollinger_bands(
    values: list[float], period: int = 20, deviations: float = 2.0
) -> dict:
    """Calculate the latest Bollinger Bands using population standard deviation."""
    if len(values) < period:
        return {"upper": None, "middle": None, "lower": None}

    window = values[-period:]
    middle = sum(window) / period
    variance = sum((value - middle) ** 2 for value in window) / period
    standard_deviation = variance ** 0.5

    return {
        "upper": middle + deviations * standard_deviation,
        "middle": middle,
        "lower": middle - deviations * standard_deviation,
    }

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
    dema9 = dema(closes, 9)
    bands = bollinger_bands(closes, 20, 2.0)
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
        "dema9": round(dema9[-1], 4) if dema9[-1] is not None else None,
        "bb_upper": round(bands["upper"], 4) if bands["upper"] is not None else None,
        "bb_middle": round(bands["middle"], 4) if bands["middle"] is not None else None,
        "bb_lower": round(bands["lower"], 4) if bands["lower"] is not None else None,
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
    """Generate a conservative multi-indicator signal with ATR risk levels."""
    if len(candles) < 35:
        raise ValueError("At least 35 candles are required.")

    values = calculate_indicators(candles)
    levels = calculate_market_levels(candles)
    supertrend = calculate_supertrend(candles, period=10, multiplier=3.0)

    close = float(candles[-1]["close"])
    atr_value = levels["atr14"]
    volumes = [float(c.get("volume", 0)) for c in candles]
    average_volume = sum(volumes[-21:-1]) / 20
    latest_volume = volumes[-1]

    volume_confirmed = (
        average_volume > 0
        and latest_volume > 0
        and latest_volume >= average_volume * 1.05
    )

    volume_analysis = {
        "source": "BiQuote tickVolume",
        "latest_tick_volume": round(latest_volume, 2),
        "average_tick_volume": round(average_volume, 2),
        "required_tick_volume": round(average_volume * 1.05, 2),
        "confirmation": "PASS" if volume_confirmed else "FAIL",
    }

    required_values = (
        values["ema9"], values["ema21"], values["dema9"],
        values["vwap"], values["macd"], values["macd_signal"],
        values["rsi14"], values["bb_middle"],
        supertrend["value"], atr_value,
    )

    if any(value is None for value in required_values) or atr_value <= 0:
        return {
            "signal": "WAIT",
            "entry": None, "stop": None,
            "target1": None, "target2": None, "target3": None,
            "indicators": values, "levels": levels,
            "supertrend": supertrend,
            "volume_confirmation": volume_confirmed,
            "volume_analysis": volume_analysis,
            "message": "Required indicator data is unavailable. WAIT.",
        }

    buy_checks = {
        "ema_trend": values["ema9"] > values["ema21"],
        "dema_trend": values["dema9"] > values["ema9"],
        "above_vwap": close > values["vwap"],
        "macd_bullish": values["macd"] > values["macd_signal"],
        "rsi_bullish": 52 <= values["rsi14"] <= 68,
        "supertrend_bullish": supertrend["trend"] == "BULLISH",
        "above_bollinger_mid": close > values["bb_middle"],
        "volume_confirmed": volume_confirmed,
    }

    sell_checks = {
        "ema_trend": values["ema9"] < values["ema21"],
        "dema_trend": values["dema9"] < values["ema9"],
        "below_vwap": close < values["vwap"],
        "macd_bearish": values["macd"] < values["macd_signal"],
        "rsi_bearish": 32 <= values["rsi14"] <= 48,
        "supertrend_bearish": supertrend["trend"] == "BEARISH",
        "below_bollinger_mid": close < values["bb_middle"],
        "volume_confirmed": volume_confirmed,
    }

    buy_score = sum(buy_checks.values())
    sell_score = sum(sell_checks.values())

    signal = "WAIT"
    entry = stop = target1 = target2 = target3 = None

    buy_mandatory = (
        buy_checks["rsi_bullish"]
        and buy_checks["ema_trend"]
        and buy_checks["supertrend_bullish"]
        and buy_checks["volume_confirmed"]
    )
    sell_mandatory = (
        sell_checks["rsi_bearish"]
        and sell_checks["ema_trend"]
        and sell_checks["supertrend_bearish"]
        and sell_checks["volume_confirmed"]
    )

    buy_support = sum(
        buy_checks[key]
        for key in ("dema_trend", "above_vwap", "macd_bullish", "above_bollinger_mid")
    )
    sell_support = sum(
        sell_checks[key]
        for key in ("dema_trend", "below_vwap", "macd_bearish", "below_bollinger_mid")
    )

    if buy_mandatory and buy_support >= 3:
        signal = "BUY"
        entry = close
        stop = entry - atr_value
        target1 = entry + atr_value
        target2 = entry + (2 * atr_value)
        target3 = entry + (3 * atr_value)

    elif sell_mandatory and sell_support >= 3:
        signal = "SELL"
        entry = close
        stop = entry + atr_value
        target1 = entry - atr_value
        target2 = entry - (2 * atr_value)
        target3 = entry - (3 * atr_value)

    if signal == "WAIT":
        message = "Indicator conditions are not sufficiently aligned. WAIT."
    else:
        message = (
            f"{signal} conditions confirmed by {max(buy_score, sell_score)}/8 checks. "
            "Educational technical signal; not a guarantee of profit."
        )

    return {
        "signal": signal,
        "entry": round(entry, 4) if entry is not None else None,
        "stop": round(stop, 4) if stop is not None else None,
        "target1": round(target1, 4) if target1 is not None else None,
        "target2": round(target2, 4) if target2 is not None else None,
        "target3": round(target3, 4) if target3 is not None else None,
        "indicators": values,
        "levels": levels,
        "supertrend": supertrend,
        "volume_confirmation": volume_confirmed,
        "volume_analysis": volume_analysis,
        "buy_score": buy_score,
        "sell_score": sell_score,
        "buy_checks": buy_checks,
        "sell_checks": sell_checks,
        "message": message,
    }


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
