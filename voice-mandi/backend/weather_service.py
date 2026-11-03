"""
Weather Service for Voice Mandi.
Fetches real-time localized weather via OpenWeather API using the configured key.
Provides dynamic temperature, rain probability, and transport risk advisories
customized to the farmer's entered village, district, or state.
"""

import os
import re
from typing import Dict, Any
import requests
from dotenv import load_dotenv
from pathlib import Path

# Ensure .env is loaded
load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Transliteration dictionary for common Indian district names in regional scripts
INDIAN_DISTRICT_MAP = {
    "पुणे": "Pune", "बारामती": "Baramati", "नाशिक": "Nashik", "सोलापूर": "Solapur",
    "मुंबई": "Mumbai", "नागपूर": "Nagpur", "कोल्हापूर": "Kolhapur", "सातारा": "Satara",
    "औरंगाबाद": "Aurangabad", "छत्रपती संभाजीनगर": "Aurangabad", "अहमदनगर": "Ahmednagar",
    "सुरत": "Surat", "સુરત": "Surat", "રાજકોટ": "Rajkot", "राजकोट": "Rajkot",
    "અમદાવાદ": "Ahmedabad", "अहमदाबाद": "Ahmedabad", "વડોદરા": "Vadodara",
    "લુધિયાણા": "Ludhiana", "ਲੁਧਿਆਣਾ": "Ludhiana", "लुधियाना": "Ludhiana",
    "ਖੰਨਾ": "Khanna", "खन्ना": "Khanna", "ਜਲੰਧਰ": "Jalandhar", "जालंधर": "Jalandhar",
    "অমৃতসর": "Amritsar", "অമൃതসর": "Amritsar", "অমৃতসর": "Amritsar",
    "கொல்கத்தா": "Kolkata", "কলকাতা": "Kolkata", "कोलकाता": "Kolkata",
    "বর্ধমান": "Bardhaman", "बर्धमान": "Bardhaman",
    "சென்னை": "Chennai", "चेन्नई": "Chennai", "கோயம்புத்தூர்": "Coimbatore", "कोयंबटूर": "Coimbatore",
    "மதுரை": "Madurai", "திண்டுக்கல்": "Dindigul",
    "హైదరాబాద్": "Hyderabad", "हैदराबाद": "Hyderabad", "వరంగల్": "Warangal", "वरंगल": "Warangal",
    "గుంటూరు": "Guntur",
    "ಬೆಂಗಳೂರು": "Bengaluru", "बेंगलुरु": "Bengaluru", "ಮೈಸೂರು": "Mysore", "ಕೋಲಾರ": "Kolar",
    "ಕೊಚ್ಚಿ": "Kochi", "കൊച്ചി": "Kochi", "पालक्काड": "Palakkad", "പാലക്കാട്": "Palakkad",
    "କଟକ": "Cuttack", "ଭୁବନେଶ୍ୱର": "Bhubaneswar", "कटक": "Cuttack", "भुवनेश्वर": "Bhubaneswar"
}

WEATHER_CONDITION_ICONS = {
    "Clear": "☀️",
    "Clouds": "⛅",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Smoke": "🌫️",
    "Haze": "🌫️",
    "Dust": "🌪️",
    "Fog": "🌫️",
    "Sand": "🌪️"
}


def clean_city_name(raw_name: str) -> str:
    """Extract clean English city/district name for OpenWeather search."""
    text = (raw_name or "").strip()
    if not text:
        return "Pune"

    # Check direct dictionary mapping
    for reg, eng in INDIAN_DISTRICT_MAP.items():
        if reg in text:
            return eng

    # If comma-separated (e.g. "Baramati, Pune"), check parts
    if "," in text:
        parts = [p.strip() for p in text.split(",")]
        for p in parts:
            for reg, eng in INDIAN_DISTRICT_MAP.items():
                if reg in p:
                    return eng
            # If part is Latin text, try first part
            clean_part = re.sub(r"[^a-zA-Z\s]", "", p).strip()
            if len(clean_part) >= 3:
                return clean_part

    # Remove non-alphanumeric except spaces
    cleaned = re.sub(r"[^a-zA-Z\s]", "", text).strip()
    return cleaned if len(cleaned) >= 3 else "Pune"


def get_regional_weather(location: str = "Pune") -> Dict[str, Any]:
    """
    Fetches real-time localized weather via OpenWeather API.
    Calculates temperature, dynamic rain probability, and transit precautions.
    """
    raw_location = (location or "Pune").strip()
    city = clean_city_name(raw_location)
    weather_key = os.getenv("WEATHER_API_KEY", "")

    # Attempt OpenWeather live API call
    if weather_key and weather_key != "mock_openweather_key":
        # Candidate cities to try: primary detected city, then fallback city
        candidates = [city]
        if city.lower() != "pune":
            candidates.append("Pune")

        for c in candidates:
            try:
                url = f"https://api.openweathermap.org/data/2.5/weather?q={c},IN&appid={weather_key}&units=metric"
                res = requests.get(url, timeout=4)
                if res.status_code == 200:
                    data = res.json()
                    temp_val = round(data.get("main", {}).get("temp", 28))
                    temp = f"{temp_val}°C"
                    humidity = data.get("main", {}).get("humidity", 40)
                    weather_main = data.get("weather", [{}])[0].get("main", "Clear")
                    weather_desc = data.get("weather", [{}])[0].get("description", "clear sky").title()
                    cloud_pct = data.get("clouds", {}).get("all", 0)

                    # Dynamic rain probability calculation
                    if weather_main.lower() in ["rain", "drizzle", "thunderstorm"]:
                        rain_prob = max(75, min(95, cloud_pct))
                    elif weather_main.lower() == "clouds":
                        rain_prob = max(25, int(cloud_pct * 0.6))
                    else:
                        rain_prob = max(5, int(cloud_pct * 0.2))

                    icon = WEATHER_CONDITION_ICONS.get(weather_main, "🌤️")

                    # Dynamic agricultural transit risk alert
                    if rain_prob >= 60:
                        risk_alert = f"Precipitation alert in {c} ({rain_prob}% rain risk). Protect transit crops with waterproof tarpaulin."
                    elif rain_prob >= 30:
                        risk_alert = f"Partly cloudy with {humidity}% humidity in {c}. Safe for transit; keep tarpaulin ready as a precaution."
                    else:
                        risk_alert = f"Clear and favorable weather in {c} ({temp}). Ideal for mandi transport, drying, and trading."

                    display_name = raw_location if raw_location else c
                    return {
                        "location": display_name,
                        "matched_city": c,
                        "temperature": temp,
                        "condition": weather_main,
                        "description": weather_desc,
                        "humidity": f"{humidity}%",
                        "cloud_cover": f"{cloud_pct}%",
                        "rain_probability_24h": f"{rain_prob}%",
                        "risk_alert": risk_alert,
                        "badge_text": f"{icon} {display_name}: {temp} {weather_desc} ({rain_prob}% Rain Risk)",
                        "is_live_api": True
                    }
            except Exception as e:
                print(f"[Weather API Exception]: {str(e)}")

    # Fallback mock if API key unavailable
    return {
        "location": raw_location,
        "matched_city": "Pune",
        "temperature": "29°C",
        "condition": "Clear",
        "description": "Clear Sky",
        "humidity": "36%",
        "cloud_cover": "10%",
        "rain_probability_24h": "10%",
        "risk_alert": f"Clear weather in {raw_location}. Favorable for crop transport and mandi sales.",
        "badge_text": f"☀️ {raw_location}: 29°C Clear Sky (10% Rain Risk)",
        "is_live_api": False
    }


if __name__ == "__main__":
    print("Testing Live Weather:")
    print("Nashik:", get_regional_weather("Nashik"))
    print("Baramati, Pune:", get_regional_weather("Baramati, Pune"))
    print("Kolkata:", get_regional_weather("Kolkata"))
    print("Surat:", get_regional_weather("Surat"))
