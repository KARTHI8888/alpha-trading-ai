const translations = {
  en: {
    language: "Language",
    workspace: "CHART ANALYSIS WORKSPACE",
    title: "Trade with a clearer view.",
    subtitle: "Upload a chart screenshot to prepare an analysis request.",
    disclaimer: "Local AI is available. Live indicators are available only for supported symbols. Signal remains WAIT; no verified trading signal is provided.",
    setup: "Set up your chart",
    manual: "MANUAL INPUT",
    market: "Market",
    timeframe: "Timeframe",
    uploadTitle: "Add chart screenshot",
    uploadDesc: "Choose an image from Gallery or use Camera.",
    chooseImage: "Choose image",
    captureChart: "Capture Chart",
    captureReady: "Chart screenshot captured successfully.",
    captureFailed: "Screenshot capture is unavailable. Open the Android app.",
    noImage: "No image selected",
    apiAddress: "Backend API address",
    analyze: "Request placeholder analysis",
    result: "Analysis result",
    waitNote: "No verified chart analysis is available. WAIT is the safe placeholder state.",
    entry: "Entry Price",
    stop: "Stop Loss",
    target1: "Target 1",
    target2: "Target 2",
    target3: "Target 3",
    notConnected: "Market data and analysis: not connected",
    planned: "Planned analysis tools",
    options: "CE BUY / PE BUY",
    plannedNote: "EMA 9/21, RSI, MACD, VWAP and Supertrend calculations are available for supported Forex/Gold symbols. ORB, CPR and CE/PE options signals are not implemented.",
    footer: "Educational project scaffold · No broker orders",
    selectImage: "Select a chart image first.",
    unsupportedImage: "Choose a PNG, JPEG, GIF, or WebP image.",
    missingApi: "Enter the backend API address.",
    sending: "Running local SmolVLM vision model…",
    success: "Local AI image processing completed. Signal remains WAIT.",
    visionResult: "Local AI image description:",
    error400: "The image is empty or the request is invalid (HTTP 400).",
    error413: "The image exceeds the 10 MiB upload or safe image-decoding limit (HTTP 413).",
    error415: "Unsupported or invalid image. Use PNG, JPEG, GIF, or WebP (HTTP 415).",
    genericError: "The API request failed",
    networkError: "Could not connect to the API. Check the address and that the backend is running.",
  },
  ta: {
    language: "மொழி",
    workspace: "விளக்கப்படப் பகுப்பாய்வுப் பணியிடம்",
    title: "தெளிவான பார்வையுடன் செயல்படுங்கள்.",
    subtitle: "பகுப்பாய்வு கோரிக்கைக்காக விளக்கப்படப் படத்தைப் பதிவேற்றவும்.",
    disclaimer: "Local AI செயல்படத் தயாராக உள்ளது. ஆதரிக்கப்படும் சந்தைகளுக்கு மட்டும் Live Indicators கிடைக்கும். சரிபார்க்கப்பட்ட வர்த்தகச் சிக்னல் இல்லை; எனவே நிலை WAIT.",
    setup: "விளக்கப்படத்தை அமைக்கவும்",
    manual: "கைமுறை உள்ளீடு",
    market: "சந்தை",
    timeframe: "கால அளவு",
    uploadTitle: "விளக்கப்படப் படத்தைச் சேர்க்கவும்",
    uploadDesc: "கேலரியிலிருந்து படத்தைத் தேர்ந்தெடுக்கவும் அல்லது கேமராவைப் பயன்படுத்தவும்.",
    chooseImage: "படத்தைத் தேர்ந்தெடுக்கவும்",
    captureChart: "விளக்கப்படத்தைப் படம் எடுக்கவும்",
    captureReady: "விளக்கப்படப் படம் வெற்றிகரமாகப் பதிவு செய்யப்பட்டது.",
    captureFailed: "Screenshot வசதி கிடைக்கவில்லை. Android App-ஐ திறக்கவும்.",
    noImage: "படம் தேர்ந்தெடுக்கப்படவில்லை",
    apiAddress: "Backend API முகவரி",
    analyze: "மாதிரி பகுப்பாய்வைக் கோரவும்",
    result: "பகுப்பாய்வு முடிவு",
    waitNote: "சரிபார்க்கப்பட்ட விளக்கப்படப் பகுப்பாய்வு கிடைக்கவில்லை. WAIT என்பது பாதுகாப்பான மாதிரி நிலை.",
    entry: "நுழைவு விலை",
    stop: "இழப்பு நிறுத்தம்",
    target1: "இலக்கு 1",
    target2: "இலக்கு 2",
    target3: "இலக்கு 3",
    notConnected: "சந்தைத் தரவும் பகுப்பாய்வும்: இணைக்கப்படவில்லை",
    planned: "திட்டமிடப்பட்ட பகுப்பாய்வுக் கருவிகள்",
    options: "CE BUY / PE BUY",
    plannedNote: "Forex/Gold சந்தைகளுக்கு EMA 9/21, RSI, MACD, VWAP, Supertrend கணக்கீடுகள் உள்ளன. ORB, CPR மற்றும் CE/PE Options signals இன்னும் உருவாக்கப்படவில்லை.",
    footer: "கல்வித் திட்டத் தொடக்கம் · Broker orders இல்லை",
    selectImage: "முதலில் விளக்கப்படப் படத்தைத் தேர்ந்தெடுக்கவும்.",
    unsupportedImage: "PNG, JPEG, GIF அல்லது WebP படத்தைத் தேர்ந்தெடுக்கவும்.",
    missingApi: "Backend API முகவரியை உள்ளிடவும்.",
    sending: "Local SmolVLM AI படத்தைப் பகுப்பாய்வு செய்கிறது…",
    success: "Local AI படச் செயலாக்கம் முடிந்தது. Signal WAIT நிலையில் உள்ளது.",
    visionResult: "Local AI பட விளக்கம்:",
    error400: "படம் காலியாக உள்ளது அல்லது கோரிக்கை தவறானது (HTTP 400).",
    error413: "படம் 10 MiB பதிவேற்ற அல்லது பாதுகாப்பான பட-decoding வரம்பை மீறுகிறது (HTTP 413).",
    error415: "ஆதரிக்கப்படாத அல்லது தவறான படம். PNG, JPEG, GIF அல்லது WebP பயன்படுத்தவும் (HTTP 415).",
    genericError: "API கோரிக்கை தோல்வியடைந்தது",
    networkError: "API-யுடன் இணைக்க முடியவில்லை. முகவரியையும் backend இயங்குகிறதா என்பதையும் சரிபார்க்கவும்.",
  },
};

const $ = (id) => document.getElementById(id);
let selectedFile = null;
let requestMessageKey = "";
let requestMessageStatus = 0;
let hasAnalysisResponse = false;

function currentLanguage() {
  return translations[$("language").value] || translations.en;
}

function renderRequestMessage() {
  const language = currentLanguage();
  const statusMessages = {
    400: language.error400,
    413: language.error413,
    415: language.error415,
  };

  let text = statusMessages[requestMessageStatus];
  if (!text && requestMessageKey) text = language[requestMessageKey];
  if (requestMessageKey === "genericError") {
    text = `${language.genericError} (HTTP ${requestMessageStatus}).`;
  }
  $("request-message").textContent = text || "";
}

function setRequestMessage(key, status = 0) {
  requestMessageKey = key;
  requestMessageStatus = status;
  renderRequestMessage();
}

function renderLanguage() {
  const languageCode = $("language").value;
  const language = currentLanguage();
  document.documentElement.lang = languageCode;
  $("language").setAttribute("aria-label", language.language);

  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const value = language[node.dataset.i18n];
    if (value) node.textContent = value;
  });

  $("file-name").textContent = selectedFile ? selectedFile.name : language.noImage;
  if (hasAnalysisResponse) $("result-note").textContent = language.success;
  renderRequestMessage();
}


function updateLiveChart() {
  const symbols = {
    XAUUSD: "OANDA:XAUUSD",
    EURUSD: "OANDA:EURUSD",
    GBPUSD: "OANDA:GBPUSD",
  };
  const intervals = { "5m": "5", "15m": "15", "30m": "30", "1h": "60" };
  const symbol = symbols[$("market").value] || "OANDA:XAUUSD";
  const interval = intervals[$("timeframe").value] || "5";
  $("live-chart").src =
    `https://www.tradingview.com/widgetembed/?symbol=${encodeURIComponent(symbol)}&interval=${interval}&timezone=Asia%2FKolkata&theme=dark&style=1&locale=en&hide_top_toolbar=false&allow_symbol_change=false&save_image=false`;
}

async function loadBackendHealth() { const base = $("api-url").value.trim().replace(/[/]+$/, ""); try { const response = await fetch(`${base}/health`); const data = await response.json(); $("local-ai-status").textContent = response.ok && data.analysis_connected ? "CONNECTED" : "DISCONNECTED"; $("broker-status").textContent = data.broker_orders_enabled ? "ENABLED" : "DISABLED"; } catch (error) { $("local-ai-status").textContent = "DISCONNECTED"; $("broker-status").textContent = "DISABLED"; } }

async function loadLiveIndicators() {
  const status = $("market-status");
  const note = $("market-data-note");
  const indicatorIds = ["ema9", "ema21", "rsi14", "macd", "macd-signal", "vwap"];
  const resultIds = ["entry", "stop", "target1", "target2", "target3"];
  const symbol = $("market").value;
  const interval = $("timeframe").value;

  function resetResult(message = "WAIT") {
    $("signal").textContent = "WAIT";
    resultIds.forEach((id) => { $(id).textContent = "—"; });
    $("result-note").textContent = message;
  }

  if (!["XAUUSD", "EURUSD", "GBPUSD"].includes(symbol)) {
    status.textContent = "UNSUPPORTED";
    $("live-ai-status").textContent = "UNSUPPORTED";
    note.textContent = "Live analysis is not supported for " + symbol + ".";
    indicatorIds.forEach((id) => { $(id).textContent = "—"; });
    resetResult("WAIT — Market not supported by the live analysis API.");
    return;
  }

  const base = $("api-url").value.trim().replace(/\/+$/, "");
  if (!base) {
    status.textContent = "ERROR";
    $("live-ai-status").textContent = "ERROR";
    note.textContent = "Enter the backend API address.";
    resetResult("WAIT — Backend API address is missing.");
    return;
  }

  status.textContent = "LOADING";
  $("live-ai-status").textContent = "LOADING";
  note.textContent = "Fetching live market analysis...";
  resetResult("Loading experimental rule-based analysis...");

  try {
    const query = new URLSearchParams({ symbol, interval });
    const response = await fetch(`${base}/technical-analysis?${query}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `HTTP ${response.status}`);
    }

    const values = data.indicators || {};
    const levels = data.levels || {};
    const st = data.supertrend || {};
    const orb = data.orb || {};
    const cpr = data.cpr || {};

    const formatValue = (value) =>
      Number.isFinite(value) ? value.toFixed(4) : "—";

    $("supertrend").textContent = formatValue(st.value);
    $("supertrend-trend").textContent = st.trend || "WAIT";

    $("orb-high").textContent = formatValue(orb.high);
    $("orb-low").textContent = formatValue(orb.low);
    $("orb-breakout").textContent = orb.breakout || orb.status || "NOT AVAILABLE";

    $("cpr-pivot").textContent = formatValue(cpr.pivot);
    $("cpr-tc").textContent = formatValue(cpr.tc);
    $("cpr-bc").textContent = formatValue(cpr.bc);

    status.textContent = data.status || "UNKNOWN";
    $("live-ai-status").textContent = data.status || "UNKNOWN";

    for (const id of indicatorIds) {
      const value = id === "macd-signal" ? values.macd_signal : values[id];
      $(id).textContent = Number.isFinite(value) ? value.toFixed(4) : "—";
    }

    const validSignal = data.status === "FRESH" &&
      ["BUY", "SELL"].includes(data.signal);

    $("signal").textContent = validSignal ? data.signal : "WAIT";

    for (const id of resultIds) {
      const value = validSignal ? data[id] : null;
      $(id).textContent = Number.isFinite(value) ? value.toFixed(4) : "—";
    }

    const levelText = Number.isFinite(levels.atr14)
      ? ` · ATR: ${levels.atr14.toFixed(4)}` : "";

    $("result-note").textContent =
      validSignal
        ? `${data.message} Experimental signal only. Verify independently.`
        : `${data.message || "No confirmed setup."} Signal: WAIT.`;

    note.textContent =
      `Latest candle: ${data.latest_candle || "unknown"} · Age: ${data.age_minutes ?? "?"} min${levelText}`;

  } catch (error) {
    status.textContent = "ERROR";
    $("live-ai-status").textContent = "ERROR";
    note.textContent = error.message || "Could not load technical analysis.";
    indicatorIds.forEach((id) => { $(id).textContent = "—"; });
    ["supertrend", "supertrend-trend", "orb-high", "orb-low",
     "cpr-pivot", "cpr-tc", "cpr-bc"].forEach((id) => { $(id).textContent = "—"; });
    $("orb-breakout").textContent = "NOT AVAILABLE";
    resetResult("WAIT — Technical analysis could not be loaded.");
  }
}

$("market").addEventListener("change", () => { updateLiveChart(); loadLiveIndicators(); });
$("timeframe").addEventListener("change", () => { updateLiveChart(); loadLiveIndicators(); });
updateLiveChart();
loadBackendHealth();
loadLiveIndicators();

// Native Android chart screenshot capture
window.onNativeChartCaptured = function (base64) {
  try {
    const binary = atob(base64);
    const bytes = new Uint8Array(binary.length);

    for (let i = 0; i < binary.length; i++) {
      bytes[i] = binary.charCodeAt(i);
    }

    const blob = new Blob([bytes], { type: "image/jpeg" });
    selectedFile = new File([blob], "chart-capture.jpg", {
      type: "image/jpeg"
    });

    $("file-name").textContent = selectedFile.name;
    const preview = $("image-preview");
    preview.src = URL.createObjectURL(selectedFile);
    preview.hidden = false; preview.style.display = "block";
    hasAnalysisResponse = false;
    $("result-note").textContent = currentLanguage().waitNote;
    setRequestMessage("");
    $("capture-message").textContent = currentLanguage().captureReady;
  } catch (error) {
    $("capture-message").textContent = currentLanguage().captureFailed;
  }
};

$("capture-chart").addEventListener("click", () => {
  if (window.AndroidBridge && window.AndroidBridge.captureChart) {
    $("capture-message").textContent = currentLanguage().sending;
    window.AndroidBridge.captureChart();
  } else {
    $("capture-message").textContent = currentLanguage().captureFailed;
  }
});

$("language").addEventListener("change", renderLanguage);
$("choose-file").addEventListener("click", () => $("chart-file").click());

$("chart-file").addEventListener("change", (event) => {
  selectedFile = event.target.files?.[0] || null;
  $("file-name").textContent = selectedFile
    ? selectedFile.name
    : currentLanguage().noImage;

  const preview = $("image-preview");

  if (selectedFile) {
    const reader = new FileReader();

    reader.onload = () => {
      preview.src = reader.result;
      preview.hidden = false;
      preview.style.display = "block";
      preview.style.visibility = "visible";
      preview.style.opacity = "1";
    };

    reader.onerror = () => {
      $("file-name").textContent = "Image preview failed";
    };

    reader.readAsDataURL(selectedFile);
  } else {
    preview.removeAttribute("src");
    preview.hidden = true;
    preview.style.display = "none";
  }

  hasAnalysisResponse = false;
  $("result-note").textContent = currentLanguage().waitNote;
  setRequestMessage("");
});

$("analyze").addEventListener("click", async () => {
  if (!selectedFile) {
    setRequestMessage("selectImage");
    return;
  }

  const supportedTypes = new Set([
    "image/png",
    "image/jpeg",
    "image/gif",
    "image/webp",
  ]);
  if (!supportedTypes.has(selectedFile.type.toLowerCase())) {
    setRequestMessage("unsupportedImage");
    return;
  }

  const base = $("api-url").value.trim().replace(/\/+$/, "");
  if (!base) {
    setRequestMessage("missingApi");
    return;
  }

  const query = new URLSearchParams({
    market: $("market").value,
    timeframe: $("timeframe").value,
  });
  const button = $("analyze");
  button.disabled = true;
  setRequestMessage("sending");

  try {
    const response = await fetch(`${base}/analyze?${query}`, {
      method: "POST",
      headers: { "Content-Type": selectedFile.type },
      body: selectedFile,
    });

    if (!response.ok) {
      if ([400, 413, 415].includes(response.status)) {
        setRequestMessage("", response.status);
      } else {
        setRequestMessage("genericError", response.status);
      }
      return;
    }

    const data = await response.json();
    $("signal").textContent = data.signal || "WAIT";
    for (const id of ["entry", "stop", "target1", "target2", "target3"]) {
      $(id).textContent = "—";
    }

    hasAnalysisResponse = true;
    $("result-note").textContent = data.vision_description ? `${currentLanguage().visionResult} ${data.vision_description}` : (data.message || currentLanguage().success);
    setRequestMessage("success");
  } catch {
    setRequestMessage("networkError");
  } finally {
    button.disabled = false;
  }
});

renderLanguage();
