const translations = {
  en: {
    language: "Language",
    workspace: "CHART ANALYSIS WORKSPACE",
    title: "Trade with a clearer view.",
    subtitle: "Upload a chart screenshot to prepare an analysis request.",
    disclaimer: "Analysis and live market data are not connected. This starter returns WAIT and is not a trading signal.",
    setup: "Set up your chart",
    manual: "MANUAL INPUT",
    market: "Market",
    timeframe: "Timeframe",
    uploadTitle: "Add chart screenshot",
    uploadDesc: "Choose an image from Gallery or use Camera.",
    chooseImage: "Choose image",
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
    plannedNote: "Listed for future development; calculations and live feeds are not implemented.",
    footer: "Educational project scaffold · No broker orders",
    selectImage: "Select a chart image first.",
    unsupportedImage: "Choose a PNG, JPEG, GIF, or WebP image.",
    missingApi: "Enter the backend API address.",
    sending: "Contacting placeholder API…",
    success: "Placeholder response received; no actual analysis was performed.",
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
    disclaimer: "பகுப்பாய்வும் நேரடி சந்தைத் தரவும் இணைக்கப்படவில்லை. இந்தத் தொடக்கத் திட்டம் WAIT எனக் காட்டும்; இது வர்த்தகச் சிக்னல் அல்ல.",
    setup: "விளக்கப்படத்தை அமைக்கவும்",
    manual: "கைமுறை உள்ளீடு",
    market: "சந்தை",
    timeframe: "கால அளவு",
    uploadTitle: "விளக்கப்படப் படத்தைச் சேர்க்கவும்",
    uploadDesc: "கேலரியிலிருந்து படத்தைத் தேர்ந்தெடுக்கவும் அல்லது கேமராவைப் பயன்படுத்தவும்.",
    chooseImage: "படத்தைத் தேர்ந்தெடுக்கவும்",
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
    plannedNote: "எதிர்கால மேம்பாட்டிற்காக பட்டியலிடப்பட்டவை; கணக்கீடு��ளும் நேரடி தரவோடைகளும் இன்னும் செயல்படுத்தப்படவில்லை.",
    footer: "கல்வித் திட்டத் தொடக்கம் · Broker orders இல்லை",
    selectImage: "முதலில் விளக்கப்படப் படத்தைத் தேர்ந்தெடுக்கவும்.",
    unsupportedImage: "PNG, JPEG, GIF அல்லது WebP படத்தைத் தேர்ந்தெடுக்கவும்.",
    missingApi: "Backend API முகவரியை உள்ளிடவும்.",
    sending: "மாதிரி API-யுடன் இணைக்கிறது…",
    success: "மாதிரி பதில் கிடைத்தது; உண்மையான பகுப்பாய்வு செய்யப்படவில்லை.",
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

$("language").addEventListener("change", renderLanguage);
$("choose-file").addEventListener("click", () => $("chart-file").click());

$("chart-file").addEventListener("change", (event) => {
  selectedFile = event.target.files?.[0] || null;
  $("file-name").textContent = selectedFile
    ? selectedFile.name
    : currentLanguage().noImage;
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

    await response.json();
    $("signal").textContent = "WAIT";
    for (const id of ["entry", "stop", "target1", "target2", "target3"]) {
      $(id).textContent = "—";
    }

    hasAnalysisResponse = true;
    $("result-note").textContent = currentLanguage().success;
    setRequestMessage("success");
  } catch {
    setRequestMessage("networkError");
  } finally {
    button.disabled = false;
  }
});

renderLanguage();
