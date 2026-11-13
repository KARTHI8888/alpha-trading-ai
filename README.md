# ALPHA TRADING AI

A mobile-friendly starter UI and FastAPI scaffold for chart screenshot analysis. This is **not** a live market-data or trading-analysis system. The API validates an image in memory, discards it, and returns `WAIT`; it does not fetch prices, calculate indicators, or place broker orders.

## Included

- Responsive dark UI with Tamil and English labels.
- Market and timeframe selectors; browser Gallery/Camera image picker support depends on the device and browser.
- FastAPI `GET /health` and placeholder `POST /analyze`.
- Raw image request body; no multipart `FormData` and no screenshot storage.
- PNG, JPEG, GIF, and WebP decoding validation using Pillow.
- Fixed 10 MiB upload cap, per-frame pixel limit, aggregate animation pixel limit, and animation frame limit.
- CORS origins read from backend environment variable `ALLOWED_ORIGINS`.
- pytest tests for API health, accepted image formats, errors, limits, and the `WAIT` response.

## Not connected or implemented

Live market data, AI/chart interpretation, RSI, MACD, VWAP, EMA 9/21, Supertrend, ORB, CPR, and CE BUY/PE BUY analysis are future work. There is no broker integration or order execution. The entry, stop-loss, and target fields remain null. Do not use this scaffold for trading decisions.

## Android setup with Termux

1. Install Termux from F-Droid or its official GitHub releases. In Termux, install Python and Git:

   ```sh
   pkg update && pkg upgrade
   pkg install python git
   ```

2. Clone the repository and install dependencies:

   ```sh
   git clone https://github.com/KARTHI8888/alpha-trading-ai.git
   cd alpha-trading-ai
   pip install -r requirements.txt
   ```

3. Start the API, bound to the phone itself:

   ```sh
   python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
   ```

4. In a second Termux session, serve the frontend:

   ```sh
   cd alpha-trading-ai
   python -m http.server 8080 --directory frontend --bind 127.0.0.1
   ```

5. Open `http://127.0.0.1:8080` in the same phone's browser. The health endpoint is `http://127.0.0.1:8000/health`. Keep both Termux processes running.

The image button uses the browser's image picker. Whether it offers Gallery, Camera, or both depends on the Android browser and device permissions. The frontend sends the selected image bytes as the raw request body with the image's MIME type as `Content-Type`; the API does not save the image. This is local development, not a production deployment. `127.0.0.1` makes the services available only on the phone itself.

## Run on a computer

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

In a second terminal:

```sh
python -m http.server 8080 --directory frontend
```

Open `http://127.0.0.1:8080`. FastAPI development docs are at `http://127.0.0.1:8000/docs`.

## Run tests

From the repository root, with the dependencies installed:

```sh
pytest -q backend/test_main.py
```

## Configuration and deployment

The backend reads `ALLOWED_ORIGINS` from the process environment. Its local default is `http://127.0.0.1:8080,http://localhost:8080`. For deployment, configure `ALLOWED_ORIGINS` in the backend host's environment settings as a comma-separated list containing the exact frontend origin(s).

Deploy the static frontend and FastAPI backend as separate services over HTTPS. Set the frontend's Backend API address field to the deployed API base URL. Configure the API host's CORS allowlist for the deployed frontend origin. The application upload cap is fixed at 10 MiB; environment configuration cannot raise it.

No API key or other secret is needed or used by this scaffold. Do not put credentials in frontend files or commit them. `.env` is ignored by Git. This project has not been deployed to or tested on a hosting provider.
