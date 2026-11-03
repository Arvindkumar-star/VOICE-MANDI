"""
Voice Mandi - FastAPI Core Pipeline
Multilingual Agricultural Advisor for Indian Farmers powered by Sarvam AI.
Supports 10 Indian Languages, Farmer Profile Inputs (Name, District, Any Crop),
Live Dynamic OpenWeather Integration, and Speech Validation with Localized Voice Prompts.
"""

import os
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any, List

import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from mandi_service import fetch_mandi_prices, detect_commodity, clean_crop_name, resolve_target_crop
from weather_service import get_regional_weather
from languages import SUPPORTED_LANGUAGES, get_language_info

# Load environment variables robustly
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")
load_dotenv()

app = FastAPI(
    title="Voice Mandi AI Backend",
    description="Multilingual Agricultural Advisor for Indian Farmers powered by Sarvam AI",
    version="2.2.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "")
SARVAM_HEADERS = {
    "api-subscription-key": SARVAM_API_KEY,
    "Content-Type": "application/json"
}


# --- 1. Saaras Speech-to-Text ---
def saaras_stt(audio_bytes: bytes, language_code: str = "hi-IN") -> str:
    """
    Calls Sarvam AI Saaras STT API with model saaras:v4.
    Converts regional audio to text transcript in the farmer's native language.
    """
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="SARVAM_API_KEY is not configured.")

    url = "https://api.sarvam.ai/speech-to-text"
    files = {"file": ("query.wav", audio_bytes, "audio/wav")}
    data = {"language_code": language_code, "model": "saaras:v4"}

    try:
        res = requests.post(
            url,
            headers={"api-subscription-key": SARVAM_API_KEY},
            files=files,
            data=data,
            timeout=15
        )
        if res.status_code != 200:
            print(f"[Saaras STT Error] Status {res.status_code}: {res.text}")
            return ""
        return res.json().get("transcript", "").strip()
    except Exception as e:
        print(f"[Saaras STT Exception]: {str(e)}")
        return ""


# --- 2. Sarvam-105B Reasoning Engine ---
def sarvam_reasoning(
    user_transcript: str,
    language_code: str = "hi-IN",
    farmer_name: str = "",
    location: str = "",
    crop: str = ""
) -> Dict[str, Any]:
    """
    Calls Sarvam AI Chat Completions with model sarvam-105b.
    Analyzes farmer query personalized with Farmer Profile (Name, Location, Any Crop).
    Strictly forces the output to match the farmer's selected language.
    """
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="SARVAM_API_KEY is not configured.")

    lang_info = get_language_info(language_code)
    target_location = location.strip() if location and location.strip() else lang_info.get("state", "Maharashtra")
    
    # Deterministically resolve the exact crop requested in query or profile
    detected_crop = resolve_target_crop(user_transcript=user_transcript, profile_crop=crop)
    prices = fetch_mandi_prices(state=target_location, commodity=detected_crop, location_name=target_location)
    weather = get_regional_weather(location=target_location)

    farmer_greeting = farmer_name.strip() if farmer_name and farmer_name.strip() else ""

    prompt = f"""
    CRITICAL MULTILINGUAL MANDATE:
    You are Voice Mandi, an empathetic agricultural market advisor for Indian farmers.
    The farmer has chosen to communicate in {lang_info['name']} ({lang_info['native']}, language code: {language_code}).
    
    ABSOLUTE REQUIREMENT:
    - You MUST write "spoken_response" and "weather_warning" ENTIRELY and EXCLUSIVELY in {lang_info['name']} ({lang_info['native']}) using {lang_info['script']} script.
    - DO NOT use Hindi or Hindi words unless the chosen language code is 'hi-IN'.
    - If the chosen language is English ('en-IN'), use 100% natural English.
    - If the chosen language is Marathi ('mr-IN'), write 100% in Marathi.
    - If the chosen language is Gujarati ('gu-IN'), write 100% in Gujarati.
    - If the chosen language is Kannada ('kn-IN'), write 100% in Kannada.
    - If the chosen language is Tamil ('ta-IN'), write 100% in Tamil.
    - If the chosen language is Telugu ('te-IN'), write 100% in Telugu.
    - If the chosen language is Bengali ('bn-IN'), write 100% in Bengali.
    - If the chosen language is Punjabi ('pa-IN'), write 100% in Punjabi.
    - If the chosen language is Malayalam ('ml-IN'), write 100% in Malayalam.
    - If the chosen language is Odia ('od-IN'), write 100% in Odia.
    
    Farmer Profile:
    - Farmer Name: {farmer_greeting or "Farmer"}
    - Entered Village / District / State: {target_location}
    - Specific Commodity Requested: {detected_crop}
    
    Farmer Spoken Query: "{user_transcript}"
    Current Live Weather in {target_location}: {json.dumps(weather, ensure_ascii=False)}
    Mandi Prices Data for {detected_crop}: {json.dumps(prices, ensure_ascii=False)}

    Instructions:
    1. If farmer name '{farmer_greeting}' is provided, address them politely in {lang_info['name']}.
    2. Advise the farmer specifically on the mandi price for {detected_crop} in ₹/kg (quintal divided by 100).
       CROP INTEGRITY MANDATE: The crop being quoted is strictly '{detected_crop}'.
       You MUST ONLY discuss '{detected_crop}'. DO NOT mention onion, wheat, or any other crop when the user asked about '{detected_crop}'. Mention '{detected_crop}' by name in {lang_info['name']}.
       MANDI SELECTION MANDATE: You MUST strictly choose 'recommended_market' from the provided 'Mandi Prices Data' list: {json.dumps([p['market'] for p in prices], ensure_ascii=False) if prices else '[]'}.
       DO NOT recommend or mention markets outside this local list. For example, if the farmer is in Chitrakoot / UP, ONLY recommend the nearby mandis provided (such as Karwi, Banda, Satna, Prayagraj) - NEVER mention Mumbai, Pune, or other distant states.
    3. Incorporate the live weather risk (rain probability {weather.get('rain_probability_24h', '10%')}, {weather.get('condition')}) and recommend protection (e.g. tarpaulin/drying).
    4. Provide an insightful "english_analysis" in English explaining the price differences for {detected_crop} among the nearby mandis listed, distance logistics, and live weather impact.
    5. Return strictly valid JSON containing:
       - "spoken_response": "3 concise sentences in {lang_info['name']} ({lang_info['script']} script) to speak back to the farmer specifically about {detected_crop}",
       - "english_analysis": "Comprehensive English analysis detailing price spread for {detected_crop} across nearby mandis, distance logistics, and live weather risk",
       - "recommended_market": "Best Mandi name selected strictly from the Mandi Prices Data list",
       - "weather_warning": "Live weather warning line in {lang_info['name']} ({lang_info['script']} script)"
    """

    models_to_try = ["sarvam-105b-conversations", "sarvam-105b"]
    endpoints = [
        "https://api.sarvam.ai/v1/chat/completions",
        "https://api.sarvam.ai/chat/completions"
    ]

    last_error = ""
    for model_name in models_to_try:
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2
        }

        for url in endpoints:
            try:
                res = requests.post(url, json=payload, headers=SARVAM_HEADERS, timeout=25)
                if res.status_code == 200:
                    msg = res.json().get("choices", [{}])[0].get("message", {})
                    content = msg.get("content")
                    if not content:
                        continue

                    clean_json_str = content.strip()
                    if "```json" in clean_json_str:
                        clean_json_str = clean_json_str.split("```json", 1)[1]
                    if "```" in clean_json_str:
                        clean_json_str = clean_json_str.split("```", 1)[0]
                    clean_json_str = clean_json_str.strip()

                    match = re.search(r"\{.*\}", clean_json_str, re.DOTALL)
                    if match:
                        clean_json_str = match.group(0)

                    parsed = json.loads(clean_json_str)
                    if "english_analysis" not in parsed:
                        best_m = parsed.get("recommended_market", "Local APMC")
                        parsed["english_analysis"] = (
                            f"Analyzed {detected_crop} market prices for {target_location}. "
                            f"Recommended {best_m} for optimal returns considering transit and weather conditions."
                        )
                    return parsed
                else:
                    last_error = f"{res.status_code}: {res.text}"
            except Exception as e:
                last_error = str(e)

    # Localized fallback response in the farmer's selected language
    print(f"[Sarvam Reasoning Warning] Fallback activated due to: {last_error}")
    best_market = max(prices, key=lambda x: x.get("price_per_kg", 0)) if prices else {"market": "Local APMC", "price_per_kg": 30}
    
    localized_fallback = lang_info.get("fallback_advice", f"Hello Farmer, current price for {detected_crop} is favorable today.")
    return {
        "spoken_response": localized_fallback,
        "english_analysis": (
            f"Analyzed {detected_crop} rates across {target_location} mandis. "
            f"Best rate observed at {best_market['market']} (₹{best_market['price_per_kg']}/kg). "
            f"Current weather: {weather.get('description', 'Clear')}, Rain probability: {weather.get('rain_probability_24h', '10%')}."
        ),
        "recommended_market": best_market["market"],
        "weather_warning": weather.get("risk_alert", "मौसम अपडेट")
    }


# --- 3. Bulbul Text-to-Speech ---
def bulbul_tts(text: str, target_language: str = "hi-IN") -> str:
    """
    Calls Sarvam AI Text-to-Speech using model bulbul:v4 (with bulbul:v3 compatibility fallback),
    speaker 'shubh', and pace 0.85, returning base64 audio in the target language.
    """
    if not SARVAM_API_KEY:
        raise HTTPException(status_code=500, detail="SARVAM_API_KEY is not configured.")

    url = "https://api.sarvam.ai/text-to-speech"
    clean_text = (text or "").strip()
    if not clean_text:
        return ""

    if len(clean_text) > 450:
        clean_text = clean_text[:450]

    models_to_try = ["bulbul:v4", "bulbul:v3", "bulbul:v4-flash"]

    for model_name in models_to_try:
        speaker_name = "shubh" if model_name in ["bulbul:v4", "bulbul:v3"] else "aayan_hi_conversational"
        payload = {
            "inputs": [clean_text],
            "target_language_code": target_language,
            "speaker": speaker_name,
            "pitch": 0,
            "pace": 0.85,
            "model": model_name
        }

        try:
            res = requests.post(url, json=payload, headers=SARVAM_HEADERS, timeout=15)
            if res.status_code == 200:
                audios = res.json().get("audios", [])
                if audios:
                    return audios[0]
            else:
                print(f"[Bulbul TTS Info] Model {model_name} ({target_language}) returned {res.status_code}: {res.text[:100]}")
        except Exception as e:
            print(f"[Bulbul TTS Exception with {model_name}]: {str(e)}")

    return ""


# --- Live Weather Endpoint ---
@app.get("/api/weather")
def get_live_weather(location: str = Query("Pune")):
    """
    Returns real live OpenWeather data for the specified village, district, or state.
    """
    weather_data = get_regional_weather(location=location)
    return weather_data


# --- Master Pipeline Route ---
@app.post("/api/voice-mandi")
async def process_farmer_voice(
    file: UploadFile = File(...),
    language_code: Optional[str] = Form("hi-IN"),
    farmer_name: Optional[str] = Form(""),
    location: Optional[str] = Form(""),
    crop: Optional[str] = Form("")
):
    """
    Master pipeline:
    1. Saaras STT: audio_bytes + language_code -> transcript
    2. Speech Validation: If audio is silent or unclear -> Polite voice prompt in chosen language!
    3. Sarvam-105B Reasoning: Personalized with Farmer Profile and Live Weather
    4. Bulbul TTS: Native regional audio response
    """
    audio_bytes = await file.read()
    clean_lang = (language_code or "hi-IN").strip()
    lang_info = get_language_info(clean_lang)
    target_location = location.strip() if location and location.strip() else lang_info.get("state", "Maharashtra")

    # Step 1: Saaras Speech-to-Text in selected language
    transcript = saaras_stt(audio_bytes, language_code=clean_lang)

    # Step 2: Clear Speech Validation & Localized Fallback
    if not transcript or len(transcript.strip()) < 2:
        fallback_crop = resolve_target_crop("", profile_crop=crop)
        unclear_msg = lang_info.get(
            "unclear_speech_prompt",
            "माफ़ कीजिए, आपकी आवाज़ साफ़ सुनाई नहीं दी। कृपया माईक दबाकर दोबारा बोलें।"
        )
        retry_audio_b64 = bulbul_tts(unclear_msg, target_language=clean_lang)
        raw_prices = fetch_mandi_prices(state=target_location, commodity=fallback_crop, location_name=target_location)
        weather = get_regional_weather(location=target_location)

        return {
            "user_transcript": "",
            "is_unclear": True,
            "ai_response": {
                "spoken_response": unclear_msg,
                "english_analysis": f"The spoken audio was silent or unintelligible. The AI gracefully requested the farmer to tap the mic and repeat clearly in {lang_info['name']}.",
                "recommended_market": "Please repeat clearly",
                "weather_warning": weather.get("risk_alert", "Check local weather")
            },
            "audio_base64": retry_audio_b64,
            "raw_prices": raw_prices,
            "weather": weather,
            "language_code": clean_lang,
            "language_info": lang_info,
            "farmer_profile": {
                "farmer_name": farmer_name,
                "location": target_location,
                "crop": fallback_crop
            }
        }

    # Step 3: Clear transcript available -> resolve exact crop from spoken query or profile!
    target_crop = resolve_target_crop(user_transcript=transcript, profile_crop=crop)
    ai_analysis = sarvam_reasoning(
        transcript,
        language_code=clean_lang,
        farmer_name=farmer_name,
        location=target_location,
        crop=target_crop
    )

    # Step 4: Bulbul Text-to-Speech in selected regional voice
    spoken_audio_b64 = bulbul_tts(ai_analysis.get("spoken_response", ""), target_language=clean_lang)
    raw_prices = fetch_mandi_prices(state=target_location, commodity=target_crop, location_name=target_location)
    weather = get_regional_weather(location=target_location)

    return {
        "user_transcript": transcript,
        "is_unclear": False,
        "ai_response": ai_analysis,
        "audio_base64": spoken_audio_b64,
        "raw_prices": raw_prices,
        "weather": weather,
        "language_code": clean_lang,
        "language_info": lang_info,
        "farmer_profile": {
            "farmer_name": farmer_name,
            "location": target_location,
            "crop": target_crop
        }
    }


# Helper Text Endpoint for Testing / Simulation
class TextQueryRequest(BaseModel):
    query: str
    language_code: Optional[str] = "hi-IN"
    farmer_name: Optional[str] = ""
    location: Optional[str] = ""
    crop: Optional[str] = ""


@app.post("/api/text-mandi")
async def process_text_query(req: TextQueryRequest):
    """Auxiliary endpoint enabling text/simulation mode across any of the 10 languages."""
    clean_lang = (req.language_code or "hi-IN").strip()
    lang_info = get_language_info(clean_lang)
    target_location = req.location.strip() if req.location and req.location.strip() else lang_info.get("state", "Maharashtra")
    weather = get_regional_weather(location=target_location)

    transcript = req.query.strip()
    if not transcript:
        fallback_crop = resolve_target_crop("", profile_crop=req.crop)
        unclear_msg = lang_info.get(
            "unclear_speech_prompt",
            "माफ़ कीजिए, आपकी आवाज़ साफ़ सुनाई नहीं दी। कृपया माईक दबाकर दोबारा बोलें।"
        )
        retry_audio_b64 = bulbul_tts(unclear_msg, target_language=clean_lang)
        raw_prices = fetch_mandi_prices(state=target_location, commodity=fallback_crop, location_name=target_location)
        return {
            "user_transcript": "",
            "is_unclear": True,
            "ai_response": {
                "spoken_response": unclear_msg,
                "english_analysis": f"The query was empty. Prompted farmer in {lang_info['name']} to speak clearly.",
                "recommended_market": "Please repeat clearly",
                "weather_warning": weather.get("risk_alert", "Check local weather")
            },
            "audio_base64": retry_audio_b64,
            "raw_prices": raw_prices,
            "weather": weather,
            "language_code": clean_lang,
            "language_info": lang_info,
            "farmer_profile": {
                "farmer_name": req.farmer_name,
                "location": target_location,
                "crop": fallback_crop
            }
        }

    # Resolve exact crop from query or profile!
    target_crop = resolve_target_crop(user_transcript=transcript, profile_crop=req.crop)
    ai_analysis = sarvam_reasoning(
        transcript,
        language_code=clean_lang,
        farmer_name=req.farmer_name or "",
        location=target_location,
        crop=target_crop
    )
    spoken_audio_b64 = bulbul_tts(ai_analysis.get("spoken_response", ""), target_language=clean_lang)
    raw_prices = fetch_mandi_prices(state=target_location, commodity=target_crop, location_name=target_location)

    return {
        "user_transcript": transcript,
        "is_unclear": False,
        "ai_response": ai_analysis,
        "audio_base64": spoken_audio_b64,
        "raw_prices": raw_prices,
        "weather": weather,
        "language_code": clean_lang,
        "language_info": lang_info,
        "farmer_profile": {
            "farmer_name": req.farmer_name,
            "location": target_location,
            "crop": target_crop
        }
    }


# Get Supported Languages API
@app.get("/api/languages")
def list_languages():
    return {
        "total_languages": len(SUPPORTED_LANGUAGES),
        "languages": SUPPORTED_LANGUAGES
    }


# Health check
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Voice Mandi AI",
        "supported_languages_count": len(SUPPORTED_LANGUAGES),
        "sarvam_api_key_configured": bool(SARVAM_API_KEY),
        "weather_api_key_configured": bool(os.getenv("WEATHER_API_KEY"))
    }


# Mount frontend static files
frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    @app.get("/")
    def serve_frontend_index():
        return FileResponse(str(frontend_dir / "index.html"))

    @app.get("/styles.css")
    def serve_styles():
        return FileResponse(str(frontend_dir / "styles.css"))

    @app.get("/app.js")
    def serve_js():
        return FileResponse(str(frontend_dir / "app.js"))

    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
