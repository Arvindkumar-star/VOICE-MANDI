import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests

sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables
load_dotenv(Path(__file__).parent / ".env")
load_dotenv(Path(__file__).parent / "backend" / ".env")
load_dotenv()

api_key = os.getenv("SARVAM_API_KEY")
print(f"Connecting to Sarvam AI with API key: {api_key[:8]}...{api_key[-4:] if api_key else 'None'}")

url = "https://api.sarvam.ai/v1/chat/completions"
headers = {
    "api-subscription-key": api_key,
    "Content-Type": "application/json"
}
payload = {
    "model": "sarvam-105b",
    "messages": [
        {"role": "user", "content": "Namaste! Are you ready to assist with Voice Mandi?"}
    ]
}

res = requests.post(url, json=payload, headers=headers)
if res.status_code == 200:
    print("Sarvam AI Response:")
    print(res.json()["choices"][0]["message"]["content"])
else:
    print(f"Sarvam API call failed ({res.status_code}): {res.text}")

