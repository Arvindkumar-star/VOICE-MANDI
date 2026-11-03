Voice Mandi: Complete Phase-by-Phase Development Guide & Village-Themed Interactive UI
This document provides a complete technical roadmap and UI/UX design blueprint for building Voice Mandi, an AI-powered agricultural advisor using Sarvam's API ecosystem.
🚀 Quick Start: Sarvam AI API Setup & Connection Test
Follow these exact steps to verify your Sarvam AI API connection before building the full Voice Mandi project:
Step 1: Install Sarvam SDK
pip install sarvamai
Step 2: Environment Configuration
Create a .env file in your root project directory:
SARVAM_API_KEY=sk_sq1ffx5v_yBM8o18a5TbepkZlcbx7rcYk
Add .env to your .gitignore file to ensure security. Read the key from the environment and never hardcode or print it in production code.
Step 3: Quick Connection Verification Script (test_sarvam.py)
import os
from dotenv import load_dotenv
from sarvamai import Sarvam

# Load environment variables
load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")

# Initialize client
client = Sarvam(api_key=api_key)

# Make a minimal chat completion call
response = client.chat.completions.create(
    model="sarvam-105b-conversations",
    messages=[
        {"role": "user", "content": "Namaste! Are you ready to assist with Voice Mandi?"}
    ]
)

# Print the model reply
print(response.choices[0].message.content)

🌾 Part 1: Village-Centric UI/UX Concept & Design Guidelines
To build an intuitive experience for farmers in rural India, the interface avoids complex text inputs, nested menus, or technical legalese.
🎨 Visual & Theme Guidelines
Color Palette: Warm Earth & Crop Tones
Primary Green: Earthy Krishi Green (#2E7D32) for actions and primary headers.
Harvest Gold: Wheat / Harvest Yellow (#FBC02D) for highlights and active audio waves.
Earth Clay: Warm Soil Brown (#795548) for subtle background accents.
Typography & Icons:
Extra-large typography in regional scripts (Hindi, Marathi, Gujarati, Kannada).
Icon-first navigation using recognizable real-life symbols (Mic 🎙️, Tractor 🚜, Wheat 🌾, Sun/Rain 🌦️, Mandi Gate 🏪).
📱 Layout Breakdown
Header Banner:
Village name tag and dynamic live weather display (e.g., "📍 Pune Region • ☀️ 29°C Clear").
Hero Feature - The "Mic Circle" (Suno Aur Bolo):
A large, glowing green microphone button centered on the screen.
High contrast text below: "माईक दबाएं और पूछें" (Press Mic & Ask).
Animated audio waveform rings (Harvest Gold) indicating active listening state.
Mandi Live Rate Ticker Card:
Clean cards displaying current local crop rates in simple units (₹/Kg instead of quintals).
Interactive Response Card:
Dual-tab output displaying Spoken Response Text in regional script alongside a simplified Mandi Comparison Table (e.g., Market Name, Price per Kg, Distance/Transport Cost).
Big "Audio Playback" button with speed control (0.8x for slow speech).
🛠️ Part 2: Step-by-Step Phase-by-Phase Coding Roadmap
Phase 1: Environment & Project Setup
1.1 Project Directory Structure
voice-mandi/
├── backend/
│   ├── main.py              # FastAPI application core
│   ├── mandi_service.py     # Live Mandi & Mock price integration
│   ├── weather_service.py   # Real-time weather API helper
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # API keys
└── frontend/
    ├── index.html           # Village UI markup
    ├── styles.css           # Rural earthy design styles
    └── app.js               # Voice recording & API connection
1.2 Dependencies (backend/requirements.txt)
t
fastapi==0.110.0
uvicorn==0.28.0
requests==2.31.0
python-multipart==0.0.9
pydantic==2.6.4
python-dotenv==1.0.1


#### 1.3 Environment Variables (`backend/.env`)

```env
SARVAM_API_KEY=your_sarvam_api_key_here
WEATHER_API_KEY=your_openweather_key_or_mock
Phase 2: Backend API & Service Integration
2.1 Mandi Price Service (backend/mandi_service.py)
import requests

def fetch_mandi_prices(state: str = "Maharashtra", commodity: str = "Onion"):
    """
    Fetches real-time Mandi price or provides structured mock data for fallback.
    """
    try:
        # Open API attempt
        url = f"https://mandi-api.vercel.app/v1/prices?state={state}&commodity={commodity}"
        res = requests.get(url, timeout=3)
        if res.status_code == 200 and res.json():
            return res.json()[:3]
    except Exception:
        pass

    # Fallback hackathon data (Price in Quintals)
    return [
        {"market": "Pune (Manjri)", "price_per_qtl": 3100, "distance_km": 15, "state": "Maharashtra"},
        {"market": "Solapur APMC", "price_per_qtl": 2650, "distance_km": 80, "state": "Maharashtra"},
        {"market": "Mumbai APMC", "price_per_qtl": 3500, "distance_km": 140, "state": "Maharashtra"}
    ]
2.2 Weather Service Integration (backend/weather_service.py)
import requests

def get_regional_weather(location: str = "Pune"):
    """
    Returns simplified weather risk alerts for transport/harvest advice.
    """
    # Mock weather payload for hackathon stability
    return {
        "location": location,
        "temperature": "28°C",
        "condition": "Rain Warning",
        "rain_probability_24h": "75%",
        "risk_alert": "Heavy rainfall expected tonight. Protect transit crops."
    }
2.3 Main FastAPI Application (backend/main.py)
import os
import json
import base64
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from mandi_service import fetch_mandi_prices
from weather_service import get_regional_weather

load_dotenv()

app = FastAPI(title="Voice Mandi AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_HEADERS = {
    "api-subscription-key": SARVAM_API_KEY,
    "Content-Type": "application/json"
}

# --- 1. Saaras Speech-to-Text ---
def saaras_stt(audio_bytes: bytes, language_code: str = "hi-IN") -> str:
    url = "https://api.sarvam.ai/speech-to-text"
    files = {"file": ("query.wav", audio_bytes, "audio/wav")}
    data = {"language_code": language_code, "model": "saaras:v4"}

    res = requests.post(
        url,
        headers={"api-subscription-key": SARVAM_API_KEY},
        files=files,
        data=data
    )
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Saaras STT Failed: {res.text}")
    return res.json().get("transcript", "")

# --- 2. Sarvam-105B Reasoning Engine ---
def sarvam_reasoning(user_transcript: str) -> dict:
    prices = fetch_mandi_prices()
    weather = get_regional_weather()

    prompt = f"""
    You are Voice Mandi (आवाज़ मंडी), an empathetic agricultural advisor for Indian farmers.
    Farmer Query: "{user_transcript}"
    Mandi Prices Data (per quintal): {prices}
    Regional Weather Info: {weather}

    Instructions:
    1. Respond in simple, natural spoken Hindi/Hinglish suitable for farmers.
    2. Convert quintal prices into price per kg (divide quintal rate by 100).
    3. Provide actionable transport advice considering weather alerts.
    4. Return strictly valid JSON containing:
       - "spoken_response": "Short text (max 3 sentences) to be spoken to the farmer",
       - "recommended_market": "Name of best Mandi",
       - "weather_warning": "Short weather alert line"
    """

    url = "https://api.sarvam.ai/chat/completions"
    payload = {
        "model": "sarvam-105b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }

    res = requests.post(url, json=payload, headers=SARVAM_HEADERS)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Sarvam-105B LLM Failed: {res.text}")

    content = res.json()["choices"][0]["message"]["content"]
    clean_json = content.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# --- 3. Bulbul Text-to-Speech ---
def bulbul_tts(text: str, target_language: str = "hi-IN") -> str:
    url = "https://api.sarvam.ai/text-to-speech"
    payload = {
        "inputs": [text],
        "target_language_code": target_language,
        "speaker": "shubh",
        "pitch": 0,
        "pace": 0.85,
        "model": "bulbul:v4"
    }

    res = requests.post(url, json=payload, headers=SARVAM_HEADERS)
    if res.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Bulbul TTS Failed: {res.text}")
    return res.json().get("audios", [""])[0]

# --- Master Pipeline Route ---
@app.post("/api/voice-mandi")
async def process_farmer_voice(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    
    # Pipeline Execution
    transcript = saaras_stt(audio_bytes)
    ai_analysis = sarvam_reasoning(transcript)
    spoken_audio_b64 = bulbul_tts(ai_analysis["spoken_response"])

    return {
        "user_transcript": transcript,
        "ai_response": ai_analysis,
        "audio_base64": spoken_audio_b64,
        "raw_prices": fetch_mandi_prices()
    }
Phase 3: Interactive Village-Themed Frontend Building
3.1 Markup (frontend/index.html)
l<!DOCTYPE html><html lang="hi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Mandi - किसान आवाज़ सहचरी</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-card">
        <!-- Village Banner -->
        <header class="header">
            <div class="village-tag">📍 पुणे ग्रामीण (Pune Village)</div>
            <div class="weather-badge">🌧️ बारिश की चेतावनी (75%)</div>
        </header>

    <main class="main-content">
        <h1 class="title">🌾 आवाज़ मंडी</h1>
        <p class="subtitle">अपनी भाषा में मंडी भाव पूछें</p>

        <!-- Big Mic Recording Circle -->
        <div class="mic-section">
            <button id="micBtn" class="mic-button">
                <span class="mic-icon">🎙️</span>
            </button>
            <div id="statusText" class="status-label">माईक दबाएं और बोलना शुरू करें</div>
        </div>

        <!-- Output Section -->
        <div id="outputCard" class="output-card hidden">
            <div class="transcript-box">
                <small>आपने पूछा:</small>
                <p id="userTranscript">"..."</p>
            </div>

            <div class="advice-box">
                <small>आवाज़ मंडी सलाह:</small>
                <p id="aiSpokenText">...</p>
            </div>

            <div class="audio-control">
                <button onclick="playAudio()" class="play-btn">🔊 फिर से सुनें (Play Audio)</button>
            </div>

            <!-- Price Table -->
            <div class="table-container">
                <h3>📊 लाइव मंडी भाव तुलना (Live Mandi Rates)</h3>
                <table id="priceTable">
                    <thead>
                        <tr>
                            <th>मंडी (Market)</th>
                            <th>भाव (Price/Kg)</th>
                            <th>दूरी (Dist)</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody"></tbody>
                </table>
            </div>
        </div>
    </main>
</div>
<script src="app.js"></script>

</body>
</html>
```
3.2 Rural Earthy Styling (frontend/styles.css)
:root {
    --primary-green: #2E7D32;
    --harvest-gold: #FBC02D;
    --earth-brown: #5D4037;
    --bg-warm: #FBF8F1;
}

body {
    background-color: var(--bg-warm);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    display: flex;
    justify-content: center;
    padding: 15px;
}

.app-card {
    background: #ffffff;
    border: 3px solid var(--primary-green);
    border-radius: 20px;
    max-width: 480px;
    width: 100%;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.header {
    display: flex;
    justify-content: space-between;
    font-weight: bold;
    font-size: 14px;
    color: var(--earth-brown);
    margin-bottom: 20px;
}

.weather-badge {
    background: #FFF3E0;
    color: #E65100;
    padding: 4px 8px;
    border-radius: 8px;
}

.title {
    text-align: center;
    color: var(--primary-green);
    margin: 0;
    font-size: 32px;
}

.subtitle {
    text-align: center;
    color: var(--earth-brown);
    margin-bottom: 30px;
}

.mic-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 30px;
}

.mic-button {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: var(--primary-green);
    border: 6px solid var(--harvest-gold);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s, background 0.2s;
    box-shadow: 0 6px 15px rgba(46, 125, 50, 0.4);
}

.mic-button.recording {
    background: #C62828;
    animation: pulse 1.2s infinite;
}

.mic-icon {
    font-size: 50px;
}

.status-label {
    margin-top: 15px;
    font-weight: bold;
    color: var(--earth-brown);
    font-size: 16px;
}

.output-card {
    background: #F1F8E9;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #A5D6A7;
}

.hidden { display: none; }

.play-btn {
    width: 100%;
    background: var(--harvest-gold);
    border: none;
    padding: 12px;
    border-radius: 8px;
    font-weight: bold;
    font-size: 16px;
    cursor: pointer;
    margin: 15px 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

th, td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #C8E6C9;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.08); }
    100% { transform: scale(1); }
}
3.3 Voice Capture Logic (frontend/app.js)
let mediaRecorder;
let audioChunks = [];
let audioBase64 = "";

const micBtn = document.getElementById('micBtn');
const statusText = document.getElementById('statusText');

micBtn.addEventListener('click', async () => {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        micBtn.classList.remove('recording');
        statusText.innerText = "प्रोसेस हो रहा है... (Processing)";
    } else {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = [];

        mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
        mediaRecorder.onstop = sendAudioToBackend;

        mediaRecorder.start();
        micBtn.classList.add('recording');
        statusText.innerText = "सुन रहे हैं... बोलना बंद करने के लिए दोबारा दबाएं";
    }
});

async function sendAudioToBackend() {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const formData = new FormData();
    formData.append('file', audioBlob, 'farmer_query.wav');

    try {
        const response = await fetch('http://localhost:8000/api/voice-mandi', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        displayResults(data);
    } catch (err) {
        statusText.innerText = "त्रुटि हुई। कृपया पुन: प्रयास करें।";
    }
}

function displayResults(data) {
    statusText.innerText = "माईक दबाएं और बोलना शुरू करें";
    document.getElementById('outputCard').classList.remove('hidden');
    document.getElementById('userTranscript').innerText = `"${data.user_transcript}"`;
    document.getElementById('aiSpokenText').innerText = data.ai_response.spoken_response;

    audioBase64 = data.audio_base64;
    playAudio();

    // Populate Price Table
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';
    data.raw_prices.forEach(row => {
        tbody.innerHTML += `
            <tr>
                <td>${row.market}</td>
                <td><b>₹${row.price_per_qtl / 100} / kg</b></td>
                <td>${row.distance_km} km</td>
            </tr>
        `;
    });
}

function playAudio() {
    if (audioBase64) {
        const audio = new Audio("data:audio/wav;base64," + audioBase64);
        audio.play();
    }
}
🎯 Summary Checklist for Development
Phase
Milestone
Primary Deliverable
Phase 1
Environment Setup
Virtualenv setup, dependencies installed, .env file populated
Phase 2
Backend & AI Pipeline
FastAPI service with Saaras STT, Sarvam-105B reasoning, Bulbul TTS
Phase 3
UI & Voice Capture
Web audio recording, responsive village UI, live Hindi audio response


