"""Safe API scaffold: no market data, analysis, persistence, or broker orders."""

import os
import warnings
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
    "http://127.0.0.1:8080,http://localhost:8080",
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
    analysis_connected: Literal[False]
    market_data_connected: Literal[False]
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
    analysis_connected: Literal[False] = False
    market_data_connected: Literal[False] = False
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


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Report API health without implying trading integrations are available."""
    return HealthResponse(
        status="ok",
        analysis_connected=False,
        market_data_connected=False,
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

    validate_decoded_image(bytes(image_data), content_type)
    image_data.clear()

    return AnalysisResponse(
        signal="WAIT",
        market=market,
        timeframe=timeframe,
        entry=None,
        stop=None,
        target1=None,
        target2=None,
        target3=None,
        message=(
            "Screenshot analysis and live market data are not implemented. "
            "WAIT is a safe placeholder, not a trading signal."
        ),
    )
