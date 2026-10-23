import os
from pathlib import Path

from dotenv import load_dotenv
from fasiri import Fasiri
from fasiri.providers import SunbirdProvider

load_dotenv(
    Path(__file__).resolve().parent / ".env",
    override=True,
)

api_key = os.getenv("SUNBIRD_API_KEY", "").strip()

if not api_key:
    raise SystemExit("Add SUNBIRD_API_KEY to your .env file.")

client = Fasiri(
    providers=[
        SunbirdProvider(api_key=api_key),
    ]
)

print("Translating English to Luganda...")

result = client.translate(
    text="Good morning. How are you?",
    source="en",
    target="lug",
)

print("Translation:", result.translated_text)
print("Provider:", result.provider)