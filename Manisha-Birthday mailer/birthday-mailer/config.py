"""
config.py — Load settings from .env (or environment variables).
Copy .env.example → .env and fill in your credentials.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if present
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# ── SMTP / Email settings ──────────────────────────────────────────────────────
EMAIL_ADDRESS: str = os.getenv("EMAIL_ADDRESS", "")
EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "")

# Gmail (default). For Outlook use smtp-mail.outlook.com / 587.
# For Yahoo use smtp.mail.yahoo.com / 587.
SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))

# ── Validation ─────────────────────────────────────────────────────────────────
if not EMAIL_ADDRESS:
    raise EnvironmentError(
        "EMAIL_ADDRESS is not set. Copy .env.example → .env and add your email."
    )
if not EMAIL_PASSWORD:
    raise EnvironmentError(
        "EMAIL_PASSWORD is not set. For Gmail, use an App Password (not your regular password).\n"
        "Generate one at: https://myaccount.google.com/apppasswords"
    )
