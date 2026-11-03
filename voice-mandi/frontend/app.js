/**
 * Voice Mandi - Frontend Application Logic
 * 1. Multilingual Support across 10 Indian Languages (strictly in selected tongue)
 * 2. Dynamic Farmer Profile with any crop (16 popular presets or custom typed crop)
 * 3. Live Dynamic OpenWeather Integration varying per entered village/district/state
 * 4. Speech Validation with polite localized voice fallback
 */

const LANGUAGES_MAP = {
    "hi-IN": {
        name: "Hindi",
        native: "हिन्दी",
        flag: "🇮🇳",
        script: "Devanagari",
        default_city: "Pune",
        village_tag: "📍 पुणे ग्रामीण (Pune Village)",
        mic_label: "माईक दबाएं और बोलना शुरू करें",
        mic_sublabel: "Press Mic & Speak your crop question in Hindi",
        sample_queries: [
            "आज मंडी में प्याज का क्या भाव है?",
            "टमाटर कहाँ बेचना सबसे फायदेमंद रहेगा?",
            "क्या आज रात बारिश में माल ले जाना सुरक्षित है?"
        ]
    },
    "mr-IN": {
        name: "Marathi",
        native: "मराठी",
        flag: "🚩",
        script: "Devanagari",
        default_city: "Pune",
        village_tag: "📍 पुणे ग्रामीण (Pune Village)",
        mic_label: "माईक दाबा आणि बोलायला सुरुवात करा",
        mic_sublabel: "Press Mic & Speak your crop question in Marathi",
        sample_queries: [
            "आज बाजारात कांद्याचा काय भाव चालू आहे?",
            "टोमॅटो कोणत्या APMC मध्ये विकणे फायदेशीर ठरेल?",
            "पावसात माल बाजारात नेणे सुरक्षित आहे का?"
        ]
    },
    "gu-IN": {
        name: "Gujarati",
        native: "ગુજરાતી",
        flag: "🌾",
        script: "Gujarati",
        default_city: "Rajkot",
        village_tag: "📍 રાજકોટ માર્કેટ (Rajkot APMC)",
        mic_label: "માઇક દબાવો અને બોલવાનું શરૂ કરો",
        mic_sublabel: "Press Mic & Speak your crop question in Gujarati",
        sample_queries: [
            "આજે માર્કેટ યાર્ડમાં ડુંગળીનો શું ભાવ છે?",
            "ટામેટા ક્યાં વેચવા સૌથી વધુ નફાકારક રહેશે?",
            "શું વરસાદમાં પાકનું પરિવહન કરવું સલામત છે?"
        ]
    },
    "kn-IN": {
        name: "Kannada",
        native: "ಕನ್ನಡ",
        flag: "🌾",
        script: "Kannada",
        default_city: "Bengaluru",
        village_tag: "📍 ಯಶವಂತಪುರ ಮಾರುಕಟ್ಟೆ (Yeshwantpur)",
        mic_label: "ಮೈಕ್ ಒತ್ತಿ ಮಾತನಾಡಲು ಪ್ರಾರಂಭಿಸಿ",
        mic_sublabel: "Press Mic & Speak your crop question in Kannada",
        sample_queries: [
            "ಇಂದು ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ಈರುಳ್ಳಿ ದರ ಎಷ್ಟಿದೆ?",
            "ಟೊಮೆಟೊ ಎಲ್ಲಿ ಮಾರಾಟ ಮಾಡುವುದು ಹೆಚ್ಚು ಲಾಭದಾಯಕ?",
            "ಮಳೆಯಲ್ಲಿ ಬೆಳೆಯನ್ನು ಸಾಗಿಸುವುದು ಸುರಕ್ಷಿತವೇ?"
        ]
    },
    "ta-IN": {
        name: "Tamil",
        native: "தமிழ்",
        flag: "🌾",
        script: "Tamil",
        default_city: "Chennai",
        village_tag: "📍 கோயம்பேடு சந்தை (Koyambedu)",
        mic_label: "மைக்கை அழுத்தி பேசத் தொடங்குங்கள்",
        mic_sublabel: "Press Mic & Speak your crop question in Tamil",
        sample_queries: [
            "இன்று சந்தையில் வெங்காய விலை என்ன?",
            "தக்காளி எங்கு விற்றால் நல்ல லாபம் கிடைக்கும்?",
            "மழையில் பயிர்களை கொண்டு செல்வது பாதுகாப்பானதா?"
        ]
    },
    "te-IN": {
        name: "Telugu",
        native: "తెలుగు",
        flag: "🌾",
        script: "Telugu",
        default_city: "Warangal",
        village_tag: "📍 వరంగల్ మార్కెట్ (Warangal APMC)",
        mic_label: "మైక్ నొక్కి మాట్లాడటం ప్రారంభించండి",
        mic_sublabel: "Press Mic & Speak your crop question in Telugu",
        sample_queries: [
            "ఈరోజు మార్కెట్లో ఉల్లిపాయ ధర ఎంత ఉంది?",
            "టమోటాలను ఎక్కడ విక్రయిస్తే ఎక్కువ లాభం వస్తుంది?",
            "వర్షంలో పంటను మార్కెట్‌కు తరలించడం సురಕ್ಷితమేనా?"
        ]
    },
    "bn-IN": {
        name: "Bengali",
        native: "বাংলা",
        flag: "🌾",
        script: "Bengali",
        default_city: "Kolkata",
        village_tag: "📍 বর্ধমান বাজার (Burdwan Market)",
        mic_label: "মাইক টিপুন এবং কথা বলা শুরু করুন",
        mic_sublabel: "Press Mic & Speak your crop question in Bengali",
        sample_queries: [
            "আজ বাজারে পেঁয়াজের দর কত চলছে?",
            "টমেটো কোথায় বিক্রি করা সবচেয়ে লাভজনক হবে?",
            "আজ বৃষ্টির মধ্যে ফসল পরিবহন করা কি নিরাপদ?"
        ]
    },
    "pa-IN": {
        name: "Punjabi",
        native: "ਪੰਜਾਬੀ",
        flag: "🌾",
        script: "Gurmukhi",
        default_city: "Ludhiana",
        village_tag: "📍 ਖੰਨਾ ਮੰਡੀ (Khanna Mandi)",
        mic_label: "ਮਾਈਕ ਦਬਾਓ ਅਤੇ ਬੋਲਣਾ ਸ਼ੁਰੂ ਕਰੋ",
        mic_sublabel: "Press Mic & Speak your crop question in Punjabi",
        sample_queries: [
            "ਅੱਜ ਮੰਡੀ ਵਿੱਚ ਪਿਆਜ਼ ਦਾ ਕੀ ਭਾਅ ਚੱਲ ਰਿਹਾ ਹੈ?",
            "ਟਮਾਟਰ ਕਿਸ ਮੰਡੀ ਵਿੱਚ ਵੇਚਣਾ ਫਾਇਦੇਮੰਦ ਰਹੇਗਾ?",
            "ਕੀ ਅੱਜ ਮੀਂਹ ਵਿੱਚ ਫ਼ਸਲ ਲਿਜਾਣਾ ਠੀਕ ਹੈ?"
        ]
    },
    "ml-IN": {
        name: "Malayalam",
        native: "മലയാളം",
        flag: "🌾",
        script: "Malayalam",
        default_city: "Kochi",
        village_tag: "📍 കൊച്ചി മാർക്കറ്റ് (Kochi Market)",
        mic_label: "മൈക്ക് അമർത്തി സംസാരിച്ചു തുടങ്ങൂ",
        mic_sublabel: "Press Mic & Speak your crop question in Malayalam",
        sample_queries: [
            "ഇന്ന് വിപണിയിൽ ഉള്ളി വില എത്രയാണ്?",
            "തക്കാളി എവിടെ വിൽക്കുന്നതാണ് കൂടുതൽ ലാഭകരം?",
            "മഴയത്ത് വിളകൾ കൊണ്ടുപോകുന്നത് സുരക്ഷിതമാണോ?"
        ]
    },
    "od-IN": {
        name: "Odia",
        native: "ଓଡ଼ିଆ",
        flag: "🌾",
        script: "Odia",
        default_city: "Cuttack",
        village_tag: "📍 କଟକ ମଣ୍ଡି (Cuttack Mandi)",
        mic_label: "ମାଇକ୍ ଦବାନ୍ତୁ ଏବଂ କହିବା ଆରମ୍ଭ କରନ୍ତୁ",
        mic_sublabel: "Press Mic & Speak your crop question in Odia",
        sample_queries: [
            "ଆଜି ମଣ୍ଡିରେ ପିଆଜ ଦର କେତେ ଅଛି?",
            "ଟମାଟର କେଉଁଠି ବିକିଲେ ଅଧିକ ଲାଭ ମିଳିବ?",
            "ବର୍ଷାରେ ଫସଲ ନେବା ସୁରକ୍ଷିତ କି?"
        ]
    },
    "en-IN": {
        name: "English",
        native: "English",
        flag: "🌐",
        script: "Latin",
        default_city: "Pune",
        village_tag: "📍 Pune Rural Market (India)",
        mic_label: "Press Mic and Start Speaking",
        mic_sublabel: "Speak your crop question in English",
        sample_queries: [
            "What is today's onion rate across nearby mandis?",
            "Where is the best market to sell tomatoes today?",
            "Is it safe to transport crops tonight given the rain alert?"
        ]
    }
};

let currentLanguage = "hi-IN";
let mediaRecorder = null;
let audioChunks = [];
let audioBase64 = "";
let currentAudio = null;
let playbackSpeed = 0.85;
let locationDebounceTimer = null;

// DOM Elements
const micBtn = document.getElementById('micBtn');
const statusText = document.getElementById('statusText');
const subStatusText = document.getElementById('subStatusText');
const soundWave = document.getElementById('soundWave');
const outputCard = document.getElementById('outputCard');
const userTranscript = document.getElementById('userTranscript');
const aiSpokenText = document.getElementById('aiSpokenText');
const englishAnalysisText = document.getElementById('englishAnalysisText');
const metaLangName = document.getElementById('metaLangName');
const metaFarmerName = document.getElementById('metaFarmerName');
const metaCrop = document.getElementById('metaCrop');
const metaLocation = document.getElementById('metaLocation');
const metaWeather = document.getElementById('metaWeather');
const playAudioBtn = document.getElementById('playAudioBtn');
const weatherWarningText = document.getElementById('weatherWarningText');
const recommendedMarketText = document.getElementById('recommendedMarketText');
const tableBody = document.getElementById('tableBody');
const villageTagText = document.getElementById('villageTagText');
const weatherBadge = document.getElementById('weatherBadge');
const activeLangBadge = document.getElementById('activeLangBadge');
const presetChipsContainer = document.getElementById('presetChipsContainer');
const languageSelect = document.getElementById('languageSelect');
const unclearSpeechBanner = document.getElementById('unclearSpeechBanner');
const unclearDesc = document.getElementById('unclearDesc');

// Farmer Profile Inputs
const farmerNameInput = document.getElementById('farmerNameInput');
const farmerLocationInput = document.getElementById('farmerLocationInput');
const farmerCropInput = document.getElementById('farmerCropInput');

// Resolve API URL across Localhost, Render, and Vercel deployments
const PRODUCTION_BACKEND_URL = "https://voice-mandi-backend.onrender.com";

const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get("backend")) {
    const cleanUrl = urlParams.get("backend").replace(/\/$/, "");
    localStorage.setItem("voice_mandi_backend", cleanUrl);
}
const storedBackend = localStorage.getItem("voice_mandi_backend") || window.RENDER_BACKEND_URL || PRODUCTION_BACKEND_URL;

const BACKEND_BASE = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? (window.location.port === "8000" ? "" : "http://localhost:8000")
    : storedBackend;

// --- Dynamic Live Weather Fetcher ---
async function fetchLiveWeather(locationName) {
    const loc = (locationName || "").trim() || LANGUAGES_MAP[currentLanguage].default_city;
    try {
        if (weatherBadge) weatherBadge.innerText = `⏳ ${loc} मौसम लोड हो रहा है...`;
        const res = await fetch(`${BACKEND_BASE}/api/weather?location=${encodeURIComponent(loc)}`);
        if (res.ok) {
            const data = await res.json();
            if (weatherBadge) {
                weatherBadge.innerText = data.badge_text || `☀️ ${loc}: ${data.temperature} (${data.rain_probability_24h} Rain Risk)`;
            }
            if (metaWeather) {
                metaWeather.innerText = `${data.condition} (${data.temperature}, ${data.rain_probability_24h} rain)`;
            }
        }
    } catch (e) {
        console.error("Live weather fetch error:", e);
    }
}

// Location Input Change Handler (Debounced)
function onLocationInputChanged() {
    const entered = farmerLocationInput ? farmerLocationInput.value.trim() : "";
    clearTimeout(locationDebounceTimer);
    locationDebounceTimer = setTimeout(() => {
        if (entered) {
            if (villageTagText) villageTagText.innerText = `📍 ${entered}`;
            fetchLiveWeather(entered);
        } else {
            const defaultCity = LANGUAGES_MAP[currentLanguage].default_city;
            if (villageTagText) villageTagText.innerText = LANGUAGES_MAP[currentLanguage].village_tag;
            fetchLiveWeather(defaultCity);
        }
    }, 450);
}

// --- Dropdown Handler ---
function handleDropdownLanguageChange(langCode) {
    selectLanguage(langCode);
}

// --- Initialize / Switch Language ---
function selectLanguage(langCode) {
    if (!LANGUAGES_MAP[langCode]) return;
    currentLanguage = langCode;
    const info = LANGUAGES_MAP[langCode];

    // Sync Dropdown
    if (languageSelect && languageSelect.value !== langCode) {
        languageSelect.value = langCode;
    }

    // Sync Pills
    document.querySelectorAll('.lang-pill').forEach(pill => {
        if (pill.getAttribute('data-lang') === langCode) {
            pill.classList.add('active');
        } else {
            pill.classList.remove('active');
        }
    });

    // Update Header Tag if not custom entered
    const userLoc = farmerLocationInput ? farmerLocationInput.value.trim() : "";
    if (userLoc) {
        if (villageTagText) villageTagText.innerText = `📍 ${userLoc}`;
        fetchLiveWeather(userLoc);
    } else {
        if (villageTagText) villageTagText.innerText = info.village_tag;
        fetchLiveWeather(info.default_city);
    }

    if (statusText) statusText.innerText = info.mic_label;
    if (subStatusText) subStatusText.innerText = info.mic_sublabel;

    if (activeLangBadge) {
        activeLangBadge.innerHTML = `<span>वर्तमान भाषा: <strong>${info.native} (${info.name}) [${langCode}]</strong> • Sarvam AI</span>`;
    }

    // Populate Dynamic Regional Sample Queries
    if (presetChipsContainer) {
        presetChipsContainer.innerHTML = '';
        info.sample_queries.forEach(q => {
            const btn = document.createElement('button');
            btn.className = 'chip';
            btn.innerText = q;
            btn.onclick = () => sendSampleQuery(q);
            presetChipsContainer.appendChild(btn);
        });
    }
}

// Initial setup on load
window.addEventListener('DOMContentLoaded', () => {
    selectLanguage("hi-IN");
    fetchLiveWeather("Pune");
});

// --- Microphone Click Handler ---
micBtn.addEventListener('click', async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        stopRecording();
    } else {
        startRecording();
    }
});

async function startRecording() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        let mimeType = 'audio/webm';
        if (MediaRecorder.isTypeSupported('audio/wav')) {
            mimeType = 'audio/wav';
        } else if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
            mimeType = 'audio/webm;codecs=opus';
        }

        mediaRecorder = new MediaRecorder(stream, { mimeType: mimeType });
        audioChunks = [];

        mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                audioChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = sendAudioToBackend;

        mediaRecorder.start();
        micBtn.classList.add('recording');
        if (soundWave) soundWave.classList.remove('hidden');

        const info = LANGUAGES_MAP[currentLanguage];
        statusText.innerText = `सुन रहे हैं... (${info.native} - Listening)`;
        if (subStatusText) subStatusText.innerText = "बोलना बंद करने के लिए दोबारा माईक दबाएं (Click to stop)";
    } catch (err) {
        console.error("Microphone access error:", err);
        statusText.innerText = "माईक अनुमति नहीं मिली (Mic Permission Needed)";
        if (subStatusText) subStatusText.innerText = "कृपया ब्राउज़र में माइक्रोफ़ोन की अनुमति दें या नीचे दिए प्रश्न चुनें";
    }
}

function stopRecording() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
    micBtn.classList.remove('recording');
    if (soundWave) soundWave.classList.add('hidden');

    const info = LANGUAGES_MAP[currentLanguage];
    statusText.innerText = `विश्लेषण जारी है... (Analyzing strictly in ${info.native})`;
    if (subStatusText) subStatusText.innerText = "Sarvam-105B Reasoning with live Mandi & OpenWeather data...";
}

// Helper: Extract Profile inputs (handles clean custom crop name)
function getFarmerProfile() {
    let rawCrop = farmerCropInput ? farmerCropInput.value.trim() : "";
    // Strip parenthetical text if user picked from datalist, e.g. "Tomato (टमाटर / टोमॅटो / தக்காளி)" -> "Tomato"
    if (rawCrop.includes("(")) {
        rawCrop = rawCrop.split("(")[0].trim();
    }

    return {
        farmer_name: farmerNameInput ? farmerNameInput.value.trim() : "",
        location: farmerLocationInput ? farmerLocationInput.value.trim() : "",
        crop: rawCrop
    };
}

// Client-side quick crop detector for synchronizing the UI
function detectCropFromQueryText(text) {
    if (!text) return null;
    const lower = text.toLowerCase();
    const cropPatterns = [
        { name: "Tomato", keys: ["tomato", "tomatoes", "tamatar", "टमाटर", "टोमॅटो", "ટામેટા", "ਟਮਾਟਰ", "টমেটো", "தக்காளி", "టమోటా", "టమోటాలు", "ಟೊಮೆಟೊ", "തക്കാളി", "ଟମାଟର"] },
        { name: "Onion", keys: ["onion", "onions", "pyaz", "pyaaz", "प्याज", "कांदा", "कांदे", "ડુંગળી", "ਪਿਆਜ਼", "পেঁয়াজ", "வெங்காயம்", "ఉల్లిపాయ", "ಈರುಳ್ಳಿ", "ഉള്ളി", "ପିଆଜ"] },
        { name: "Potato", keys: ["potato", "potatoes", "aloo", "alu", "आलू", "बटाटा", "બટાકા", "ਆਲੂ", "আলু", "உருளைக்கிழங்கு", "బంగాళాదుంప", "ಆಲೂಗಡ್ಡೆ", "ഉരുളക്കിഴങ്ങ്", "ଆଳୁ"] },
        { name: "Wheat", keys: ["wheat", "gehun", "gehu", "गेहूँ", "गहू", "ઘઉં", "ਕਣਕ", "গম", "கோதுமை", "గోధుమ", "ಗೋಧಿ", "ഗോതമ്പ്", "ଗହମ"] },
        { name: "Cotton", keys: ["cotton", "kapas", "kapus", "कपास", "कापूस", "કપાસ", "ਨਰਮਾ", "తులా", "பருத்தி", "పత్తి", "ಹತ್ತಿ", "പരുത്തി", "କପା"] }
    ];
    for (const cp of cropPatterns) {
        if (cp.keys.some(k => lower.includes(k))) {
            return cp.name;
        }
    }
    return null;
}

// --- Send Voice Recording to Backend ---
async function sendAudioToBackend() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const profile = getFarmerProfile();
    const formData = new FormData();

    formData.append('file', audioBlob, 'farmer_query.wav');
    formData.append('language_code', currentLanguage);
    formData.append('farmer_name', profile.farmer_name);
    formData.append('location', profile.location);
    formData.append('crop', profile.crop);

    try {
        const response = await fetch(`${BACKEND_BASE}/api/voice-mandi`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (err) {
        console.error("Fetch error:", err);
        statusText.innerText = "त्रुटि हुई। कृपया पुनः प्रयास करें।";
        if (subStatusText) subStatusText.innerText = "कृपया सुनिश्चित करें कि बैकएंड सर्वर पोर्ट 8000 पर चालू है।";
    }
}

// --- Sample Query Preset Trigger ---
async function sendSampleQuery(queryText) {
    const info = LANGUAGES_MAP[currentLanguage];

    // Auto-synchronize UI crop field if this query asks about a specific crop
    const detected = detectCropFromQueryText(queryText);
    if (detected && farmerCropInput) {
        farmerCropInput.value = detected;
    }

    const profile = getFarmerProfile();
    if (detected) {
        profile.crop = detected;
    }

    statusText.innerText = `विश्लेषण कर रहे हैं... (Thinking in ${info.native})`;
    if (subStatusText) subStatusText.innerText = `Sarvam-105B analyzing ${profile.crop || 'crop'} rates with live weather...`;

    try {
        const response = await fetch(`${BACKEND_BASE}/api/text-mandi`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                query: queryText,
                language_code: currentLanguage,
                farmer_name: profile.farmer_name,
                location: profile.location,
                crop: profile.crop
            })
        });

        if (!response.ok) {
            throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (err) {
        console.error("Sample query error:", err);
        statusText.innerText = "त्रुटि हुई। कृपया पुनः प्रयास करें।";
        if (subStatusText) subStatusText.innerText = "बैकएंड से कनेक्ट नहीं हो सका (Check port 8000)";
    }
}

// --- Display Results in UI ---
function displayResults(data) {
    const info = LANGUAGES_MAP[currentLanguage];
    statusText.innerText = info.mic_label;
    if (subStatusText) subStatusText.innerText = info.mic_sublabel;

    outputCard.classList.remove('hidden');

    // Feature 3: Clear Speech Validation Banner
    if (data.is_unclear) {
        if (unclearSpeechBanner) {
            unclearSpeechBanner.classList.remove('hidden');
            if (unclearDesc) {
                unclearDesc.innerText = data.ai_response.spoken_response;
            }
        }
        userTranscript.innerText = "⚠️ [आवाज़ स्पष्ट सुनाई नहीं दी / No clear speech detected]";
    } else {
        if (unclearSpeechBanner) {
            unclearSpeechBanner.classList.add('hidden');
        }
        userTranscript.innerText = `"${data.user_transcript || ''}"`;
    }

    // Populate Metadata strip
    const profileName = data.farmer_profile?.farmer_name || (farmerNameInput ? farmerNameInput.value.trim() : "") || "किसान भाई";
    const locName = data.farmer_profile?.location || "Regional Mandi";
    const activeCrop = data.farmer_profile?.crop || "Onion";
    if (metaFarmerName) metaFarmerName.innerText = profileName;
    if (metaCrop) metaCrop.innerText = activeCrop;
    if (metaLangName) metaLangName.innerText = `${info.name} (${currentLanguage})`;
    if (metaLocation) metaLocation.innerText = locName;
    if (farmerCropInput && (!farmerCropInput.value || !farmerCropInput.value.trim())) {
        farmerCropInput.value = activeCrop;
    }

    // Update Live Weather if returned
    if (data.weather) {
        const w = data.weather;
        if (metaWeather) metaWeather.innerText = `${w.condition} (${w.temperature}, ${w.rain_probability_24h} rain)`;
        if (weatherBadge) weatherBadge.innerText = w.badge_text || `${w.temperature} ${w.condition}`;
    }

    // Populate Spoken Response in Farmer's Chosen Language
    const aiResp = data.ai_response || {};
    aiSpokenText.innerText = aiResp.spoken_response || "";

    // Populate English Intelligence Analysis
    if (englishAnalysisText) {
        englishAnalysisText.innerText = aiResp.english_analysis || "";
    }

    // Populate Weather Alert
    if (weatherWarningText && aiResp.weather_warning) {
        weatherWarningText.innerText = aiResp.weather_warning;
    }

    // Populate Recommended Market
    if (recommendedMarketText && aiResp.recommended_market) {
        recommendedMarketText.innerText = aiResp.recommended_market;
    }

    // Populate Price Comparison Table
    tableBody.innerHTML = '';
    const prices = data.raw_prices || [];
    prices.forEach(row => {
        const kgRate = row.price_per_kg || (row.price_per_qtl / 100);
        tableBody.innerHTML += `
            <tr>
                <td><strong>${row.market}</strong><br><small style="color:#689F38">${row.commodity} • ${row.state || ''}</small></td>
                <td><b>₹${kgRate} / kg</b></td>
                <td>₹${row.price_per_qtl} / क्विंटल</td>
                <td>${row.distance_km} किमी</td>
            </tr>
        `;
    });

    // Auto-scroll to results smoothly
    outputCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Store & Play Audio in Selected Regional Voice
    audioBase64 = data.audio_base64 || "";
    if (audioBase64) {
        playAudio();
    }
}

// --- Audio Playback Logic ---
function playAudio() {
    if (!audioBase64) {
        alert("कोई ऑडियो उपलब्ध नहीं है (No audio returned)");
        return;
    }

    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    try {
        currentAudio = new Audio("data:audio/wav;base64," + audioBase64);
        currentAudio.playbackRate = playbackSpeed;

        if (playAudioBtn) {
            playAudioBtn.classList.add('playing');
            playAudioBtn.innerHTML = `<span>🔊</span> <span>आवाज़ चल रही है (Playing Voice)...</span>`;
        }

        currentAudio.onended = () => {
            if (playAudioBtn) {
                playAudioBtn.classList.remove('playing');
                playAudioBtn.innerHTML = `<span>🔊</span> <span>फिर से सुनें (Play Audio)</span>`;
            }
        };

        currentAudio.play().catch(e => {
            console.log("Autoplay was prevented by browser:", e);
            if (playAudioBtn) {
                playAudioBtn.classList.remove('playing');
                playAudioBtn.innerHTML = `<span>🔊</span> <span>फिर से सुनें (Play Audio)</span>`;
            }
        });
    } catch (e) {
        console.error("Audio playback error:", e);
    }
}

function updatePlaybackSpeed() {
    const sel = document.getElementById('speedSelect');
    if (sel) {
        playbackSpeed = parseFloat(sel.value) || 0.85;
        if (currentAudio) {
            currentAudio.playbackRate = playbackSpeed;
        }
    }
}
