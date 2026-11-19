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
    plannedNote: "Forex/Gold indicators: EMA 9/21, DEMA 9, RSI 14, MACD, VWAP, Bollinger Bands, Supertrend, ATR 14, Support and Resistance. Trading signals are not verified; WAIT is shown.",
    backtestTitle: "Historical Backtest Dashboard",
    backtestIntro: "Historical strategy results. Not a live trading signal.",
    backtestTimeframe: "Backtest timeframe",
    backtestTarget: "Target scenario",
    grossPnl: "Gross PnL (R)", netPnl: "Net PnL (R)",
    grossWinRate: "Gross Win Rate", netWinRate: "Net Win Rate",
    netProfitFactor: "Net Profit Factor", netDrawdown: "Net Max Drawdown (R)",
    closedTrades: "Closed Trades", openTrades: "Open Trades",
    dataRange: "Data range", candlesTested: "Candles tested",
    costStatus: "Execution costs", tradeDetails: "Trade details",
    tradeTime: "Entry time", tradeSide: "Side", tradeEntry: "Entry",
    tradeExit: "Exit", tradeStop: "Stop", tradeTarget: "Target",
    tradeOutcome: "Outcome", tradeNetPnl: "Net PnL",
    backtestDisclaimer: "Historical and experimental results. Costs may be disabled. MID OHLC is not Bid/Ask execution data.",
    backtestLoading: "Loading backtest report...",
    backtestLoaded: "Backtest report loaded.",
    backtestError: "Could not load backtest report.",
    costsDisabled: "DISABLED", costsEnabled: "ENABLED",
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
    plannedNote: "Forex/Gold குறியீடுகள்: EMA 9/21, DEMA 9, RSI 14, MACD, VWAP, Bollinger Bands, Supertrend, ATR 14, Support மற்றும் Resistance. Trading signal உறுதிப்படுத்தப்படவில்லை; WAIT காட்டப்படும்.",
    backtestTitle: "வரலாற்று Backtest Dashboard",
    backtestIntro: "வரலாற்று உத்தி முடிவுகள். இது Live Trading Signal அல்ல.",
    backtestTimeframe: "Backtest கால அளவு",
    backtestTarget: "இலக்கு நிலை",
    grossPnl: "மொத்த PnL (R)", netPnl: "நிகர PnL (R)",
    grossWinRate: "மொத்த வெற்றி விகிதம்", netWinRate: "நிகர வெற்றி விகிதம்",
    netProfitFactor: "நிகர Profit Factor", netDrawdown: "அதிகபட்ச நிகர Drawdown (R)",
    closedTrades: "முடிக்கப்பட்ட Trades", openTrades: "திறந்த Trades",
    dataRange: "தரவு கால வரம்பு", candlesTested: "சோதிக்கப்பட்ட Candles",
    costStatus: "செயலாக்கச் செலவுகள்", tradeDetails: "Trade விவரங்கள்",
    tradeTime: "Entry நேரம்", tradeSide: "வகை", tradeEntry: "Entry",
    tradeExit: "Exit", tradeStop: "Stop Loss", tradeTarget: "Target",
    tradeOutcome: "முடிவு", tradeNetPnl: "நிகர PnL",
    backtestDisclaimer: "இவை வரலாற்று மற்றும் சோதனை முடிவுகள். செலவுகள் முடக்கப்பட்டிருக்கலாம். MID OHLC என்பது Bid/Ask execution தரவு அல்ல.",
    backtestLoading: "Backtest அறிக்கை ஏற்றப்படுகிறது...",
    backtestLoaded: "Backtest அறிக்கை ஏற்றப்பட்டது.",
    backtestError: "Backtest அறிக்கையை ஏற்ற முடியவில்லை.",
    costsDisabled: "முடக்கப்பட்டுள்ளது", costsEnabled: "செயல்பாட்டில் உள்ளது",
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
let visionDescription = "";

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
  if (hasAnalysisResponse) {
    $("vision-insight").textContent = `${language.visionResult} ${visionDescription}`;
    $("vision-insight").hidden = false;
  }
  renderRequestMessage();
}



async function loadBacktestResults() {
  const status = $("backtest-status");
  const base = $("api-url").value.trim().replace(/\/+$/, "");
  const interval = $("backtest-interval").value;
  const target = $("backtest-target").value;
  const language = currentLanguage();

  status.textContent = language.backtestLoading;

  try {
    const response = await fetch(
      `${base}/backtest-results?interval=${encodeURIComponent(interval)}`
    );
    const data = await response.json();

    if (!response.ok) throw new Error(data.detail || language.backtestError);

    const scenario = data.scenarios?.[target];
    const m = scenario?.metrics;
    if (!m) throw new Error(language.backtestError);

    const fmt = (value, digits = 2) =>
      value === null || value === undefined || !Number.isFinite(Number(value))
        ? "—" : Number(value).toFixed(digits);

    $("bt-gross-pnl").textContent =
      `${fmt(Number(m.gross_profit_r || 0) - Number(m.gross_loss_r || 0))} R`;
    $("bt-net-pnl").textContent = `${fmt(m.net_profit_r)} R`;
    $("bt-gross-win-rate").textContent = `${fmt(m.win_rate_percent)}%`;
    $("bt-net-win-rate").textContent = `${fmt(m.net_win_rate_percent)}%`;
    $("bt-profit-factor").textContent = fmt(m.net_profit_factor);
    $("bt-drawdown").textContent = `${fmt(m.net_max_drawdown_r)} R`;
    $("bt-closed-trades").textContent = m.closed_trades ?? "—";
    $("bt-open-trades").textContent = m.open_trades ?? "—";

    $("bt-data-range").textContent =
      `${data.first_candle || "—"} → ${data.last_candle || "—"}`;
    $("bt-candles").textContent = data.candles_tested ?? "—";

    const costs = data.methodology?.costs || {};
    $("bt-cost-status").textContent =
      costs.status === "DISABLED" ? language.costsDisabled :
      costs.status === "ENABLED" ? language.costsEnabled : "—";

    $("bt-cost-details").textContent =
      `Spread: ${fmt(costs.spread_price, 4)} · Slippage/side: ${fmt(costs.slippage_per_side, 4)} · Commission: ${fmt(costs.commission_price_equivalent, 4)}. ${costs.limitations || ""}`;

    const tbody = $("backtest-trades-body");
    tbody.replaceChildren();

    const trades = Array.isArray(scenario.trades) ? scenario.trades : [];
    if (!trades.length) {
      const row = document.createElement("tr");
      const cell = document.createElement("td");
      cell.colSpan = 8;
      cell.textContent = "—";
      row.appendChild(cell);
      tbody.appendChild(row);
    } else {
      for (const trade of trades) {
        const row = document.createElement("tr");
        const values = [
          trade.entry_time || "—",
          trade.signal || "—",
          fmt(trade.entry, 4),
          fmt(trade.exit, 4),
          fmt(trade.stop_price, 4),
          fmt(trade.target_price, 4),
          trade.outcome || "—",
          `${fmt(trade.net_pnl, 4)}`
        ];
        for (const value of values) {
          const cell = document.createElement("td");
          cell.textContent = String(value);
          row.appendChild(cell);
        }
        tbody.appendChild(row);
      }
    }

    status.textContent = `${language.backtestLoaded} · ${data.symbol} · ${interval.toUpperCase()} · ${target.toUpperCase()}`;
  } catch (error) {
    status.textContent = `${language.backtestError} ${error.message || ""}`;
  }
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
  const indicatorIds = ["ema9","ema21","dema9","rsi14","macd","macd-signal","vwap","bb-upper","bb-middle","bb-lower","supertrend","supertrend-trend","atr14","support","resistance"];
  const resultIds = ["entry", "stop", "target1", "target2", "target3"];
  const symbol = $("market").value;
  const interval = $("timeframe").value;

  function resetResult(message = "WAIT") {
    $("signal").textContent = "WAIT";
    $("signal").dataset.status = "WAIT";
    $("signal-status").textContent = "WAIT";
    resultIds.forEach((id) => { $(id).textContent = "—"; });
    $("result-note").textContent = message;

    ["latest-tick-volume", "average-tick-volume", "required-tick-volume"].forEach((id) => {
      $(id).textContent = "—";
    });
    $("volume-confirmation").textContent = "—";
    $("volume-confirmation").dataset.status = "UNKNOWN";
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
    const volume = data.volume_analysis || {};
    $("latest-tick-volume").textContent =
      Number.isFinite(volume.latest_tick_volume) ? volume.latest_tick_volume.toFixed(2) : "—";
    $("average-tick-volume").textContent =
      Number.isFinite(volume.average_tick_volume) ? volume.average_tick_volume.toFixed(2) : "—";
    $("required-tick-volume").textContent =
      Number.isFinite(volume.required_tick_volume) ? volume.required_tick_volume.toFixed(2) : "—";

    const volumeStatus = $("volume-confirmation");
    volumeStatus.textContent = volume.confirmation || "—";
    volumeStatus.dataset.status = volume.confirmation || "UNKNOWN";
    status.textContent = data.status || "UNKNOWN";
    $("live-ai-status").textContent = data.status || "UNKNOWN";

    for (const id of indicatorIds) {
      const map = {"macd-signal":values.macd_signal,"bb-upper":values.bb_upper,"bb-middle":values.bb_middle,"bb-lower":values.bb_lower,"supertrend":st.value,"supertrend-trend":st.trend,"atr14":levels.atr14,"support":levels.support,"resistance":levels.resistance};
      const value = Object.prototype.hasOwnProperty.call(map,id) ? map[id] : values[id];
      $(id).textContent = Number.isFinite(value) ? value.toFixed(4) : (id === "supertrend-trend" ? (value || "WAIT") : "—");
    }

    const conditionGroups = [
      { name: "buy", checks: data.buy_checks || {}, score: data.buy_score },
      { name: "sell", checks: data.sell_checks || {}, score: data.sell_score }
    ];

    for (const group of conditionGroups) {
      const scoreElement = $(`${group.name}-score`);
      scoreElement.textContent =
        Number.isFinite(group.score) ? `${group.score} / 8` : "— / 8";

      const percentElement = $(`${group.name}-percent`);
      const progressElement = $(`${group.name}-progress`);

      if (percentElement && progressElement) {
        const validScore = Number.isFinite(group.score);
        const percent = validScore
          ? Math.round(Math.max(0, Math.min(8, group.score)) / 8 * 100)
          : 0;

        percentElement.textContent = validScore ? `${percent}%` : "—%";
        progressElement.style.width = `${percent}%`;
        progressElement.dataset.status =
          !validScore ? "UNKNOWN" : percent >= 75 ? "PASS" : "FAIL";
      }

      for (const [key, passed] of Object.entries(group.checks)) {
        const element = $(`${group.name}-${key}`);
        if (!element) continue;

        element.textContent = passed ? "PASS" : "FAIL";
        element.dataset.status = passed ? "PASS" : "FAIL";
      }
    }

    const allowedSignals = ["BUY", "SELL", "WAIT"];
    const signal = data.status === "FRESH" && allowedSignals.includes(data.signal)
      ? data.signal
      : "WAIT";

    $("signal").textContent = signal;
    $("signal").dataset.status = signal;
    $("signal-status").textContent = signal;

    const resultValues = {
      entry: data.entry,
      stop: data.stop,
      target1: data.target1,
      target2: data.target2,
      target3: data.target3
    };

    for (const id of resultIds) {
      const value = resultValues[id];
      $(id).textContent =
        signal !== "WAIT" && Number.isFinite(value) ? value.toFixed(4) : "—";
    }

    const levelText = Number.isFinite(levels.atr14)
      ? ` · ATR: ${levels.atr14.toFixed(4)}` : "";

    $("result-note").textContent = signal === "WAIT"
      ? (data.message || "WAIT — Trading conditions are not sufficiently aligned.")
      : `${data.message || signal} · Experimental rule-based signal; not a guarantee of profit.`;

    note.textContent =
      `Latest candle: ${data.latest_candle || "unknown"} · Age: ${data.age_minutes ?? "?"} min${levelText}`;

  } catch (error) {
    status.textContent = "ERROR";
    $("live-ai-status").textContent = "ERROR";
    note.textContent = error.message || "Could not load technical analysis.";
    indicatorIds.forEach((id) => { $(id).textContent = "—"; });
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
    const imageUrl = URL.createObjectURL(selectedFile);
    preview.onload = () => {
      preview.hidden = false;
      preview.style.display = "block";
      preview.style.visibility = "visible";
      preview.style.opacity = "1";
      $("capture-message").textContent =
        currentLanguage().captureReady + " (" + preview.naturalWidth + "×" + preview.naturalHeight + ")";
    };
    preview.onerror = () => {
      $("capture-message").textContent = "Captured image preview could not be displayed.";
    };
    preview.src = imageUrl;
    preview.hidden = false;
    preview.style.display = "block";
    preview.style.visibility = "visible";
    preview.style.opacity = "1";
    hasAnalysisResponse = false;
    visionDescription = "";
    $("vision-insight").textContent = "";
    $("vision-insight").hidden = true;
    setRequestMessage("");
    $("capture-message").textContent = currentLanguage().captureReady;
  } catch (error) {
    $("capture-message").textContent = currentLanguage().captureFailed;
  }
};

$("capture-chart").addEventListener("click", () => {
  const chart = $("live-chart").closest(".chart-frame");
  const rect = chart.getBoundingClientRect();
  if (window.AndroidBridge && window.AndroidBridge.captureChart && rect.width > 0 && rect.height > 0) {
    $("capture-message").textContent = currentLanguage().sending;
    window.AndroidBridge.captureChart(rect.left, rect.top, rect.width, rect.height);
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
  visionDescription = "";
  $("vision-insight").textContent = "";
  $("vision-insight").hidden = true;
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
    visionDescription = data.vision_description || data.message || currentLanguage().success;
    hasAnalysisResponse = true;
    $("vision-insight").textContent = `${currentLanguage().visionResult} ${visionDescription}`;
    $("vision-insight").hidden = false;
    setRequestMessage("success");
  } catch {
    setRequestMessage("networkError");
  } finally {
    button.disabled = false;
  }
});


$("backtest-interval").addEventListener("change", loadBacktestResults);
$("backtest-target").addEventListener("change", loadBacktestResults);
$("api-url").addEventListener("change", loadBacktestResults);

renderLanguage();
loadBacktestResults();
