import os
from pathlib import Path

import requests
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

api_key = os.getenv("SUNBIRD_API_KEY", "").strip()

print("Environment file exists:", env_path.is_file())
print("API key loaded:", bool(api_key))
print("Key includes Bearer prefix:", api_key.lower().startswith("bearer "))

if not api_key:
    raise SystemExit("Add SUNBIRD_API_KEY to your .env file.")

try:
    response = requests.post(
        "https://api.sunbird.ai/tasks/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "sunflower-9b",
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Explain what a computer is in two short sentences."
                    ),
                }
            ],
            "temperature": 0.3,
            "max_tokens": 150,
        },
        timeout=90,
    )

    if response.status_code == 401:
        print("Authentication error:", response.text[:500])

    response.raise_for_status()


    data = response.json()
    print(data["choices"][0]["message"]["content"])

except requests.HTTPError:
    print(f"Sunbird returned HTTP {response.status_code}.")
except requests.RequestException as error:
    print(f"Connection failed: {error}")
except (ValueError, KeyError, IndexError):
    print("Sunbird returned an unexpected response format.")