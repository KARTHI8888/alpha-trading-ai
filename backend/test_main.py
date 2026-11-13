from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.main import MAX_UPLOAD_BYTES, app

client = TestClient(app)
QUERY = {"market": "XAUUSD", "timeframe": "5m"}


def make_image(image_format: str, size: tuple[int, int] = (2, 2)) -> bytes:
    output = BytesIO()
    Image.new("RGB", size=size, color=(30, 120, 200)).save(
        output,
        format=image_format,
    )
    return output.getvalue()


def make_animated_gif(frame_count: int, size: tuple[int, int] = (2, 2)) -> bytes:
    frames = [
        Image.new("RGB", size=size, color=(index * 30 % 255, 80, 120))
        for index in range(frame_count)
    ]
    output = BytesIO()
    frames[0].save(
        output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
    )
    return output.getvalue()


def post_image(data: bytes, content_type: str):
    return client.post(
        "/analyze",
        params=QUERY,
        content=data,
        headers={"content-type": content_type},
    )


def test_health_returns_ok_and_reports_unconnected_integrations():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "analysis_connected": False,
        "market_data_connected": False,
        "broker_orders_enabled": False,
    }


@pytest.mark.parametrize(
    ("content_type", "image_format"),
    [
        ("image/png", "PNG"),
        ("image/jpeg", "JPEG"),
        ("image/gif", "GIF"),
        ("image/webp", "WEBP"),
    ],
)
def test_supported_decoded_images_return_wait_and_null_price_levels(
    content_type: str,
    image_format: str,
):
    response = post_image(make_image(image_format), content_type)

    assert response.status_code == 200
    result = response.json()
    assert result["signal"] == "WAIT"
    assert result["entry"] is None
    assert result["stop"] is None
    assert result["target1"] is None
    assert result["target2"] is None
    assert result["target3"] is None


def test_invalid_image_data_is_rejected():
    response = post_image(b"not an actual PNG image", "image/png")

    assert response.status_code == 415


def test_empty_upload_is_rejected():
    response = post_image(b"", "image/png")

    assert response.status_code == 400


def test_unsupported_content_type_is_rejected():
    response = post_image(b"some bytes", "text/plain")

    assert response.status_code == 415


def test_upload_over_10_mib_is_rejected():
    oversized = b"x" * (MAX_UPLOAD_BYTES + 1)
    response = post_image(oversized, "image/png")

    assert response.status_code == 413


def test_per_frame_pixel_limit_is_enforced(monkeypatch: pytest.MonkeyPatch):
    from backend import main

    monkeypatch.setattr(main, "MAX_IMAGE_PIXELS", 3)
    response = post_image(make_image("PNG", size=(2, 2)), "image/png")

    assert response.status_code == 413


def test_total_frame_pixel_limit_is_enforced(monkeypatch: pytest.MonkeyPatch):
    from backend import main

    monkeypatch.setattr(main, "MAX_IMAGE_PIXELS", 100)
    monkeypatch.setattr(main, "MAX_TOTAL_FRAME_PIXELS", 7)
    response = post_image(make_animated_gif(frame_count=2), "image/gif")

    assert response.status_code == 413


def test_animation_frame_limit_is_enforced(monkeypatch: pytest.MonkeyPatch):
    from backend import main

    monkeypatch.setattr(main, "MAX_IMAGE_FRAMES", 1)
    response = post_image(make_animated_gif(frame_count=2), "image/gif")

    assert response.status_code == 413
