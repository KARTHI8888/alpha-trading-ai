"""Safe API scaffold: no market data, analysis, persistence, or broker orders."""

import os
import json
import asyncio
import shutil
import subprocess
import tempfile
import warnings
from pathlib import Path
from enum import Enum
from io import BytesIO
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

# Fixed application limit. Environment variables cannot increase it.
MAX_UPLOAD_BYTES = 10 * 1024 * 1024

# Limits on decoded content, separate from the compressed upload byte limit.
MAX_IMAGE_PIXELS = 20_000_000
MAX_TOTAL_FRAME_PIXELS = 40_000_000
MAX_IMAGE_FRAMES = 100

MIME_FORMATS = {
    "image/png": "PNG",
    "image/jpeg": "JPEG",
    "image/gif": "GIF",
    "image/webp": "WEBP",
}

origins_setting = os.getenv(
    "ALLOWED_ORIGINS",
    "null,http://127.0.0.1:8080,http://localhost:8080",
)
allowed_origins = [
    origin.strip() for origin in origins_setting.split(",") if origin.strip()
]

app = FastAPI(
    title="ALPHA TRADING AI API",
    description="Starter API; live market data and screenshot analysis are not connected.",
    version="0.1.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class Market(str, Enum):
    XAUUSD = "XAUUSD"
    EURUSD = "EURUSD"
    GBPUSD = "GBPUSD"
    NIFTY = "NIFTY"
    BANKNIFTY = "BANKNIFTY"
    SENSEX = "SENSEX"


class Timeframe(str, Enum):
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"


class HealthResponse(BaseModel):
    status: Literal["ok"]
    analysis_connected: bool = False
    market_data_connected: bool = False
    broker_orders_enabled: Literal[False]


class AnalysisResponse(BaseModel):
    signal: Literal["WAIT"]
    market: Market
    timeframe: Timeframe
    entry: None = None
    stop: None = None
    target1: None = None
    target2: None = None
    target3: None = None
    analysis_connected: bool = False
    vision_description: str | None = None
    market_data_connected: bool = False
    broker_orders_enabled: Literal[False] = False
    message: str


def validate_decoded_image(data: bytes, content_type: str) -> None:
    """Verify and fully decode a supported image in memory within safety caps."""
    expected_format = MIME_FORMATS.get(content_type)
    if expected_format is None:
        raise HTTPException(
            status_code=415,
            detail="Content-Type must be PNG, JPEG, GIF, or WebP.",
        )

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("error", Image.DecompressionBombWarning)

            with Image.open(BytesIO(data)) as image:
                if image.format != expected_format:
                    raise HTTPException(
                        status_code=415,
                        detail="Image content does not match its Content-Type.",
                    )
                image.verify()

            with Image.open(BytesIO(data)) as image:
                if image.format != expected_format:
                    raise HTTPException(
                        status_code=415,
                        detail="Image content does not match its Content-Type.",
                    )

                frame_count = getattr(image, "n_frames", 1)
                if frame_count > MAX_IMAGE_FRAMES:
                    raise HTTPException(
                        status_code=413,
                        detail="Image has too many frames to validate safely.",
                    )

                total_pixels = 0
                for frame_number in range(frame_count):
                    image.seek(frame_number)
                    width, height = image.size
                    frame_pixels = width * height

                    if width <= 0 or height <= 0 or frame_pixels > MAX_IMAGE_PIXELS:
                        raise HTTPException(
                            status_code=413,
                            detail="Image dimensions exceed the safe decoding limit.",
                        )

                    total_pixels += frame_pixels
                    if total_pixels > MAX_TOTAL_FRAME_PIXELS:
                        raise HTTPException(
                            status_code=413,
                            detail="Image exceeds the safe total decoded-pixel limit.",
                        )

                    image.load()

    except HTTPException:
        raise
    except (
        Image.DecompressionBombError,
        Image.DecompressionBombWarning,
    ) as exc:
        raise HTTPException(
            status_code=413,
            detail="Image exceeds the safe decoding limits.",
        ) from exc
    except (UnidentifiedImageError, OSError, SyntaxError, ValueError) as exc:
        raise HTTPException(
            status_code=415,
            detail="Image data is invalid or cannot be decoded.",
        ) from exc


def run_local_vision(image_data: bytes) -> str:
    """Describe an uploaded chart using the local SmolVLM model."""
    root = Path(__file__).resolve().parent.parent
    model = root / "models" / "SmolVLM-500M-Instruct-Q8_0.gguf"
    projector = root / "models" / "mmproj-SmolVLM-500M-Instruct-Q8_0.gguf"
    executable = shutil.which("llama-mtmd-cli")
    if not executable or not model.is_file() or not projector.is_file():
        raise HTTPException(status_code=503, detail="Local vision model files or runtime unavailable.")
    temp_path = None
    try:
        with Image.open(BytesIO(image_data)) as image:
            image.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp:
                temp_path = temp.name
            image.convert("RGB").save(temp_path, format="PNG")
        prompt = ("Describe visible chart facts only: candle colors and overall "
                  "left-to-right direction if clear. Do not invent prices, "
                  "indicators, entry, stop loss, targets, or trading advice. "
                  "If unclear, say UNCLEAR.")
        result = subprocess.run(
            [executable, "-m", str(model), "--mmproj", str(projector),
             "--image", temp_path, "-p", prompt, "-c", "2048", "-n", "120",
             "-t", "4", "--no-warmup", "--temp", "0", "--top-k", "1",
             "--seed", "42"],
            capture_output=True, text=True, timeout=180,
        )
        if result.returncode != 0:
            raise HTTPException(status_code=503, detail="Local vision inference failed.")
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            raise HTTPException(status_code=503, detail="Vision model returned no description.")
        return lines[-1][:1000]
    except subprocess.TimeoutExpired as exc:
        raise HTTPException(status_code=504, detail="Vision analysis timed out.") from exc
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)



@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report local vision availability without implying trading signals."""
    root = Path(__file__).resolve().parent.parent
    model = root / "models" / "SmolVLM-500M-Instruct-Q8_0.gguf"
    projector = root / "models" / "mmproj-SmolVLM-500M-Instruct-Q8_0.gguf"
    analysis_ready = shutil.which("llama-mtmd-cli") is not None and model.is_file() and projector.is_file()
    market_data_ready = False
    try:
        from urllib.request import Request, urlopen

        url = "https://biquote.io/api/XAUUSD/ohlc?interval=5m&limit=50"
        request = Request(url, headers={"User-Agent": "ALPHA-TRADING-AI/1.0"})
        with urlopen(request, timeout=8) as response:
            payload = json.loads(response.read().decode("utf-8"))

        bars = payload.get("bars", [])
        if len(bars) >= 35:
            latest = bars[-1]
            market_data_ready = all(
                key in latest and float(latest[key]) > 0
                for key in ("open", "high", "low", "close")
            )
    except Exception:
        market_data_ready = False

    return HealthResponse(
        status="ok",
        analysis_connected=analysis_ready,
        market_data_connected=market_data_ready,
        broker_orders_enabled=False,
    )


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_screenshot(
    request: Request,
    market: Market,
    timeframe: Timeframe,
) -> AnalysisResponse:
    """Validate a raw image body in memory, discard it, and return WAIT."""
    content_type = (
        request.headers.get("content-type", "")
        .split(";", 1)[0]
        .strip()
        .lower()
    )
    if content_type not in MIME_FORMATS:
        raise HTTPException(
            status_code=415,
            detail="Content-Type must be PNG, JPEG, GIF, or WebP.",
        )

    image_data = bytearray()
    try:
        async for chunk in request.stream():
            if len(image_data) + len(chunk) > MAX_UPLOAD_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail="Image exceeds the 10 MiB upload limit.",
                )
            image_data.extend(chunk)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Could not read image request.") from exc

    if not image_data:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")

    image_bytes = bytes(image_data)
    validate_decoded_image(image_bytes, content_type)
    image_data.clear()
    vision_description = await asyncio.to_thread(run_local_vision, image_bytes)
    del image_bytes

    return AnalysisResponse(
        signal="WAIT",
        market=market,
        timeframe=timeframe,
        entry=None,
        stop=None,
        target1=None,
        target2=None,
        target3=None,
        analysis_connected=True,
        vision_description=vision_description,
        message="Local vision description only. Signal remains WAIT; no validated trading signal is provided.",
    )


class CandleInput(BaseModel):
    open: float
    high: float
    low: float
    close: float
    volume: float


class IndicatorRequest(BaseModel):
    candles: list[CandleInput]


@app.post("/indicators")
def indicators_endpoint(payload: IndicatorRequest):
    """Calculate technical indicators from user-supplied candle data."""
    from backend.indicators import calculate_indicators

    try:
        candles = [candle.model_dump() for candle in payload.candles]
        result = calculate_indicators(candles)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "signal": "WAIT",
        "indicators": result,
        "message": "Indicator calculations only. No live market data or trading signal is connected.",
    }


@app.get("/live-indicators")
def live_indicators(symbol: str = "XAUUSD", interval: str = "5m"):
    """Fetch public OHLC data and calculate indicators; never invent a trade signal."""
    import json
    from datetime import datetime, timezone
    from urllib.request import Request, urlopen

    from backend.indicators import (
        calculate_indicators,
        calculate_market_levels,
        calculate_supertrend,
    )

    allowed_symbols = {"XAUUSD", "EURUSD", "GBPUSD"}
    allowed_intervals = {"5m", "15m", "30m", "1h"}

    symbol = symbol.upper()
    if symbol not in allowed_symbols:
        raise HTTPException(status_code=400, detail="Unsupported symbol.")
    if interval not in allowed_intervals:
        raise HTTPException(status_code=400, detail="Unsupported interval.")

    url = (
        f"https://biquote.io/api/{symbol}/ohlc"
        f"?interval={interval}&limit=50"
    )
    request = Request(url, headers={"User-Agent": "ALPHA-TRADING-AI/1.0"})

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))
        bars = payload.get("bars", [])
        if len(bars) < 35:
            raise HTTPException(
                status_code=503,
                detail="Not enough candle data to calculate indicators.",
            )

        bars = sorted(bars, key=lambda bar: bar["openTime"])
        candles = [
            {
                "open": float(bar["open"]),
                "high": float(bar["high"]),
                "low": float(bar["low"]),
                "close": float(bar["close"]),
                "volume": float(bar.get("tickVolume", bar.get("volume", 0))),
            }
            for bar in bars
        ]
        indicators = calculate_indicators(candles)
        levels = calculate_market_levels(candles)
        supertrend = calculate_supertrend(candles, period=10, multiplier=3.0)

        volumes = [c["volume"] for c in candles]
        average_volume = sum(volumes[-21:-1]) / 20
        latest_volume = volumes[-1]
        volume_confirmed = (
            average_volume > 0
            and latest_volume > 0
            and latest_volume >= average_volume * 1.05
        )
        latest_time = datetime.fromisoformat(
            bars[-1]["openTime"].replace("Z", "+00:00")
        )
        age_minutes = (
            datetime.now(timezone.utc) - latest_time
        ).total_seconds() / 60

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve valid market data.",
        ) from exc

    interval_minutes = {"5m": 5, "15m": 15, "30m": 30, "1h": 60}[interval]
    is_fresh = 0 <= age_minutes <= interval_minutes * 3

    return {
        "symbol": symbol,
        "interval": interval,
        "status": "FRESH" if is_fresh else "STALE",
        "latest_candle": bars[-1]["openTime"],
        "age_minutes": round(age_minutes, 1),
        "candles_received": len(candles),
        "signal": "WAIT",
        "indicators": indicators,
        "levels": levels,
        "supertrend": supertrend,
        "volume_confirmation": volume_confirmed,
        "volume_analysis": {
            "source": "BiQuote tickVolume",
            "latest_tick_volume": round(latest_volume, 2),
            "average_tick_volume": round(average_volume, 2),
            "required_tick_volume": round(average_volume * 1.05, 2),
            "confirmation": "PASS" if volume_confirmed else "FAIL",
        },
        "message": (
            "Data freshness check passed. Indicator values only; no validated trading signal."
            if is_fresh
            else "Market data is stale. WAIT; do not use these values as a live signal."
        ),
    }


@app.get("/technical-analysis")
def technical_analysis(symbol: str = "XAUUSD", interval: str = "5m"):
    """Experimental rule-based analysis using public OHLC data."""
    import json
    from datetime import datetime, timezone
    from urllib.request import Request, urlopen
    from backend.indicators import analyze_candles

    symbol = symbol.upper()
    allowed_symbols = {"XAUUSD", "EURUSD", "GBPUSD"}
    allowed_intervals = {"5m", "15m", "30m", "1h"}

    if symbol not in allowed_symbols or interval not in allowed_intervals:
        raise HTTPException(status_code=400, detail="Unsupported symbol or interval.")

    url = f"https://biquote.io/api/{symbol}/ohlc?interval={interval}&limit=50"
    request = Request(url, headers={"User-Agent": "ALPHA-TRADING-AI/1.0"})

    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

        bars = sorted(payload.get("bars", []), key=lambda bar: bar["openTime"])
        if len(bars) < 35:
            raise HTTPException(status_code=503, detail="Not enough candle data.")

        candles = [{
            "open": float(b["open"]),
            "high": float(b["high"]),
            "low": float(b["low"]),
            "close": float(b["close"]),
            "volume": float(b.get("tickVolume", b.get("volume", 0))),
        } for b in bars]

        latest = datetime.fromisoformat(bars[-1]["openTime"].replace("Z", "+00:00"))
        age = (datetime.now(timezone.utc) - latest).total_seconds() / 60
        interval_minutes = {"5m": 5, "15m": 15, "30m": 30, "1h": 60}[interval]
        fresh = 0 <= age <= interval_minutes * 3

        result = analyze_candles(candles)
        if not fresh:
            result.update({
                "signal": "WAIT", "entry": None, "stop": None,
                "target1": None, "target2": None, "target3": None,
                "message": "Market data is stale. WAIT.",
            })

        return {
            "symbol": symbol,
            "interval": interval,
            "status": "FRESH" if fresh else "STALE",
            "latest_candle": bars[-1]["openTime"],
            "age_minutes": round(age, 1),
            **result,
            "orb": {
                "status": "NOT_AVAILABLE",
                "reason": "Requires verified Indian market opening-session candles."
            },
            "cpr": {
                "status": "NOT_AVAILABLE",
                "reason": "Requires previous completed trading-day OHLC."
            },
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Technical analysis failed.") from exc


@app.get("/indian-indices")
def indian_indices():
    """Experimental NIFTY, BANKNIFTY and SENSEX ORB/CPR calculations."""
    import json
    from datetime import datetime, timezone, timedelta
    from zoneinfo import ZoneInfo
    from urllib.request import Request, urlopen
    from urllib.parse import quote
    from backend.indicators import calculate_orb, calculate_cpr

    ist = ZoneInfo("Asia/Kolkata")
    now = datetime.now(ist)

    symbols = {
        "NIFTY": "^NSEI",
        "BANKNIFTY": "^NSEBANK",
        "SENSEX": "^BSESN",
    }

    def fetch_chart(symbol, period, interval):
        url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            f"{quote(symbol, safe='')}?range={period}&interval={interval}"
        )
        request = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 ALPHA-TRADING-AI"}
        )
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8"))

        chart = payload.get("chart", {})
        if chart.get("error") or not chart.get("result"):
            raise ValueError("Yahoo Finance returned no chart data.")

        return chart["result"][0]

    def candle_rows(result):
        timestamps = result.get("timestamp") or []
        quote_data = result["indicators"]["quote"][0]
        rows = []

        for i, stamp in enumerate(timestamps):
            values = {
                key: quote_data.get(key, [None] * len(timestamps))[i]
                for key in ("open", "high", "low", "close", "volume")
            }

            if any(values[k] is None for k in ("open", "high", "low", "close")):
                continue

            rows.append({
                "time": datetime.fromtimestamp(stamp, timezone.utc).astimezone(ist),
                "open": float(values["open"]),
                "high": float(values["high"]),
                "low": float(values["low"]),
                "close": float(values["close"]),
                "volume": float(values["volume"] or 0),
            })

        return rows

    output = {}

    for name, yahoo_symbol in symbols.items():
        try:
            intraday_result = fetch_chart(yahoo_symbol, "5d", "5m")
            intraday_rows = candle_rows(intraday_result)

            # Exclude candles that have not completed yet.
            completed = [
                row for row in intraday_rows
                if row["time"] + timedelta(minutes=5) <= now
            ]

            today_rows = [
                row for row in completed
                if row["time"].date() == now.date()
            ]

            opening_rows = [
                row for row in today_rows
                if row["time"].hour == 9
                and row["time"].minute in (15, 20, 25)
            ]

            expected_times = [(9, 15), (9, 20), (9, 25)]
            actual_times = [
                (row["time"].hour, row["time"].minute)
                for row in opening_rows
            ]

            if actual_times == expected_times:
                post_open = [
                    row for row in today_rows
                    if row["time"].hour > 9
                    or (row["time"].hour == 9 and row["time"].minute >= 30)
                ]

                if post_open:
                    orb_candles = [
                        {
                            "high": row["high"],
                            "low": row["low"],
                            "close": row["close"],
                        }
                        for row in opening_rows + post_open
                    ]
                    orb = calculate_orb(orb_candles)
                else:
                    orb = {
                        "status": "WAIT",
                        "high": round(max(r["high"] for r in opening_rows), 4),
                        "low": round(min(r["low"] for r in opening_rows), 4),
                        "breakout": "WAIT",
                        "reason": "Waiting for a completed candle after 9:30 AM IST.",
                    }
            else:
                orb = {
                    "status": "NOT_AVAILABLE",
                    "high": None,
                    "low": None,
                    "breakout": "WAIT",
                    "reason": "Complete 9:15, 9:20 and 9:25 IST candles are required.",
                }

            if completed:
                latest = completed[-1]["time"]
                age_minutes = (now - latest - timedelta(minutes=5)).total_seconds() / 60
                market_status = (
                    "FRESH" if 0 <= age_minutes <= 15 else "STALE"
                )
            else:
                age_minutes = None
                market_status = "NOT_AVAILABLE"

            if market_status != "FRESH":
                orb["breakout"] = "WAIT"
                orb["status"] = "STALE" if market_status == "STALE" else "NOT_AVAILABLE"

            # CPR uses the latest completed daily candle before today's date.
            daily_result = fetch_chart(yahoo_symbol, "1mo", "1d")
            daily_rows = candle_rows(daily_result)

            previous_days = [
                row for row in daily_rows
                if row["time"].date() < now.date()
            ]

            if previous_days:
                previous = previous_days[-1]
                cpr = calculate_cpr(
                    previous["high"],
                    previous["low"],
                    previous["close"],
                )
                cpr["previous_trading_day"] = previous["time"].date().isoformat()
            else:
                cpr = {
                    "status": "NOT_AVAILABLE",
                    "reason": "Previous completed daily OHLC is unavailable.",
                }

            output[name] = {
                "symbol": yahoo_symbol,
                "market_status": market_status,
                "age_minutes": (
                    round(age_minutes, 1) if age_minutes is not None else None
                ),
                "orb": orb,
                "cpr": cpr,
                "signal": "WAIT",
                "message": "ORB/CPR calculations only. No verified trading signal.",
            }

        except Exception as exc:
            output[name] = {
                "market_status": "NOT_AVAILABLE",
                "orb": {"status": "NOT_AVAILABLE", "breakout": "WAIT"},
                "cpr": {"status": "NOT_AVAILABLE"},
                "signal": "WAIT",
                "error": str(exc)[:200],
            }

    return {
        "timestamp_ist": now.isoformat(),
        "opening_range": "09:15-09:30 IST",
        "indices": output,
        "broker_orders_enabled": False,
    }


@app.get("/backtest-results")
async def get_backtest_results(interval: Literal["1h", "4h", "1d"] = "1h"):
    """Return an allowlisted XAUUSD historical backtest report."""
    report_files = {
        "1h": "xauusd_1h_backtest.json",
        "4h": "xauusd_4h_backtest.json",
        "1d": "xauusd_1d_backtest.json",
    }

    report_path = (
        Path(__file__).resolve().parent.parent
        / "reports"
        / report_files[interval]
    )

    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Backtest report not found.")
    except (OSError, json.JSONDecodeError):
        raise HTTPException(status_code=500, detail="Backtest report could not be read.")

    if (
        not isinstance(report, dict)
        or report.get("symbol") != "XAUUSD"
        or report.get("interval") != interval
        or not isinstance(report.get("scenarios"), dict)
        or not isinstance(report.get("methodology"), dict)
    ):
        raise HTTPException(status_code=500, detail="Backtest report format is invalid.")

    return report
