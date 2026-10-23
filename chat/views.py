# import json
# import logging
# import os

# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from django.shortcuts import render
# from django.views.decorators.http import require_POST
# from dotenv import load_dotenv
# from fasiri import Fasiri
# from fasiri.providers import SunbirdProvider


# load_dotenv(settings.BASE_DIR / ".env", override=True)

# logger = logging.getLogger(__name__)

# LANGUAGES = {"en", "lug", "nyn", "sw"}


# def index(request):
#     return render(request, "chat/index.html")


# @require_POST
# def send_message(request):
#     # Read and validate the browser's request.
#     try:
#         data = json.loads(request.body)
#     except (ValueError, UnicodeDecodeError):
#         return JsonResponse({"error": "Invalid request."}, status=400)

#     if not isinstance(data, dict):
#         return JsonResponse({"error": "Invalid request."}, status=400)

#     message = data.get("message")
#     language = data.get("language", "en")

#     if not isinstance(message, str) or not message.strip():
#         return JsonResponse(
#             {"error": "Please enter a message."},
#             status=400,
#         )

#     message = message.strip()

#     if len(message) > 2000:
#         return JsonResponse(
#             {"error": "Please keep your message under 2,000 characters."},
#             status=400,
#         )

#     if not isinstance(language, str) or language not in LANGUAGES:
#         return JsonResponse(
#             {"error": "Please select a supported language."},
#             status=400,
#         )

#     api_key = os.getenv("SUNBIRD_API_KEY", "").strip()

#     if not api_key:
#         return JsonResponse(
#             {"error": "SUNBIRD_API_KEY is missing from .env."},
#             status=503,
#         )

#     stage = "setup"

#     try:
#         fasiri_client = Fasiri(
#             providers=[
#                 SunbirdProvider(api_key=api_key),
#             ]
#         )

#         # Translate the user's message into English.
#         stage = "input translation"
#         english_message = message

#         if language != "en":
#             translation = fasiri_client.translate(
#                 text=message,
#                 source=language,
#                 target="en",
#                 provider="sunbird",
#             )
#             english_message = translation.translated_text

#         # Keep history in English for the model.
#         # Switching languages starts a fresh conversation.
#         history = request.session.get("chat_history", [])

#         if request.session.get("chat_language") != language:
#             history = []

#         conversation = [
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a helpful assistant in a DevFest demo. "
#                     "Answer in English using clear, concise language. "
#                     "Keep answers under 120 words. "
#                     "If you do not know something, say so. "
#                     "Do not claim access to live information."
#                 ),
#             },
#             *history[-12:],
#             {
#                 "role": "user",
#                 "content": english_message,
#             },
#         ]

#         # Ask Sunflower to generate an answer.
#         stage = "answer generation"

#         response = requests.post(
#             "https://api.sunbird.ai/tasks/chat/completions",
#             headers={
#                 "Authorization": f"Bearer {api_key}",
#                 "Content-Type": "application/json",
#             },
#             json={
#                 "model": "sunflower-9b",
#                 "messages": conversation,
#                 "temperature": 0.3,
#                 "max_tokens": 300,
#             },
#             timeout=90,
#         )

#         response.raise_for_status()

#         english_reply = (
#             response.json()["choices"][0]["message"]["content"]
#         )

#         if not isinstance(english_reply, str) or not english_reply.strip():
#             raise ValueError("Empty model response")

#         english_reply = english_reply.strip()

#         # Translate the answer into the selected language.
#         stage = "reply translation"
#         reply = english_reply

#         if language != "en":
#             translation = fasiri_client.translate(
#                 text=english_reply,
#                 source="en",
#                 target=language,
#                 provider="sunbird",
#             )
#             reply = translation.translated_text

#         # Save successful exchanges only.
#         request.session["chat_history"] = (
#             history
#             + [
#                 {"role": "user", "content": english_message},
#                 {"role": "assistant", "content": english_reply},
#             ]
#         )[-12:]

#         request.session["chat_language"] = language

#         return JsonResponse({"reply": reply})

#     except Exception as error:
#         # Keep credentials and provider responses out of the browser.
#         logger.error(
#             "Chat failed during %s (%s)",
#             stage,
#             type(error).__name__,
#         )

#         return JsonResponse(
#             {
#                 "error": (
#                     f"The request failed during {stage}. "
#                     "Please try again and check the Django terminal."
#                 )
#             },
#             status=502,
#         )

import json
import logging
import os

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from dotenv import load_dotenv
from fasiri import Fasiri
from fasiri.providers import SunbirdProvider


load_dotenv(settings.BASE_DIR / ".env", override=True)

logger = logging.getLogger(__name__)

# Start with English and Luganda, which you have already tested.
LANGUAGES = {"en", "lug"}


def index(request):
    return render(request, "chat/index.html")


@require_POST
def translate_text(request):
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid request."},
            status=400,
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {"error": "Invalid request."},
            status=400,
        )

    text = data.get("text")
    source = data.get("source", "en")
    target = data.get("target", "lug")

    if not isinstance(text, str) or not text.strip():
        return JsonResponse(
            {"error": "Please enter text to translate."},
            status=400,
        )

    text = text.strip()

    if len(text) > 2000:
        return JsonResponse(
            {"error": "Please enter no more than 2,000 characters."},
            status=400,
        )

    if (
        not isinstance(source, str)
        or not isinstance(target, str)
        or source not in LANGUAGES
        or target not in LANGUAGES
    ):
        return JsonResponse(
            {"error": "Please select supported languages."},
            status=400,
        )

    if source == target:
        return JsonResponse(
            {"error": "Choose different source and target languages."},
            status=400,
        )

    api_key = os.getenv("SUNBIRD_API_KEY", "").strip()

    if not api_key:
        return JsonResponse(
            {"error": "SUNBIRD_API_KEY is missing from .env."},
            status=503,
        )

    try:
        client = Fasiri(
            providers=[
                SunbirdProvider(api_key=api_key),
            ]
        )

        result = client.translate(
            text=text,
            source=source,
            target=target,
            provider="sunbird",
        )

        translated_text = result.translated_text

        if not isinstance(translated_text, str) or not translated_text.strip():
            raise ValueError("Empty translation")

        return JsonResponse(
            {
                "translation": translated_text.strip(),
                "provider": result.provider,
            }
        )

    except Exception as error:
        logger.error(
            "Translation failed (%s)",
            type(error).__name__,
        )

        return JsonResponse(
            {
                "error": (
                    "Translation failed. Please try again. "
                    "If it continues, check your Sunbird key and connection."
                )
            },
            status=502,
        )