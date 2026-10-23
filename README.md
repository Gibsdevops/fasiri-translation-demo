# Fasiri Translation Demo

A Django application demonstrating English–Luganda translation using
the Fasiri Python SDK in Direct Mode with Sunbird AI.

## Features

- English-to-Luganda and Luganda-to-English translation
- Source and target language selection
- Copy translation button
- Responsive interface

## Setup

Requires Python 3.10 or later.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Add your Sunbird API key to `.env`.

```powershell
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/.

## How it works

The browser sends text and language choices to Django.
Django calls the Fasiri SDK, which connects directly to Sunbird AI
using the configured provider key and returns the translation.

## Resources

- Website: https://www.fasiri-ai.com/
- Documentation: https://fasiri.readthedocs.io/en/latest/

Machine translations may contain errors.