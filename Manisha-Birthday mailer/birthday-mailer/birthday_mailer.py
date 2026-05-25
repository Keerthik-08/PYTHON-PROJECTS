"""
🎂 Birthday Mailer - Automated Birthday Email Sender
=====================================================
Reads contacts from data/contacts.json, checks for today's birthdays,
and sends personalized emails automatically.

Usage:
    python birthday_mailer.py              # Send emails for today's birthdays
    python birthday_mailer.py --dry-run    # Preview emails without sending
    python birthday_mailer.py --test       # Send a test email to yourself
    python birthday_mailer.py --list       # List all upcoming birthdays
"""

import json
import smtplib
import logging
import argparse
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from config import EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT
from template_engine import render_template

# ── Logging setup ─────────────────────────────────────────────────────────────
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "birthday_mailer.log"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)

# ── Data helpers ───────────────────────────────────────────────────────────────

CONTACTS_FILE = Path("data/contacts.json")


def load_contacts() -> list[dict]:
    """Load contacts from the JSON file."""
    if not CONTACTS_FILE.exists():
        log.error("contacts.json not found. Copy data/contacts.example.json → data/contacts.json and fill it in.")
        return []
    with CONTACTS_FILE.open() as f:
        return json.load(f)


def is_birthday_today(dob_str: str) -> bool:
    """Return True if today matches the month/day of the given DOB (YYYY-MM-DD)."""
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        return dob.month == today.month and dob.day == today.day
    except ValueError:
        log.warning("Invalid date format: %s (expected YYYY-MM-DD)", dob_str)
        return False


def calculate_age(dob_str: str) -> int | None:
    """Calculate age from DOB string."""
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        today = date.today()
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    except ValueError:
        return None


def upcoming_birthdays(contacts: list[dict], days: int = 30) -> list[dict]:
    """Return contacts with birthdays in the next `days` days, sorted by date."""
    today = date.today()
    upcoming = []
    for c in contacts:
        try:
            dob = datetime.strptime(c["dob"], "%Y-%m-%d").date()
            next_bday = dob.replace(year=today.year)
            if next_bday < today:
                next_bday = next_bday.replace(year=today.year + 1)
            diff = (next_bday - today).days
            if diff <= days:
                upcoming.append({**c, "_days_until": diff, "_next_bday": next_bday})
        except (ValueError, KeyError):
            continue
    return sorted(upcoming, key=lambda x: x["_days_until"])


# ── Email sending ──────────────────────────────────────────────────────────────

def send_email(to_address: str, subject: str, html_body: str, text_body: str, dry_run: bool = False) -> bool:
    """Send a MIME multipart email. Returns True on success."""
    msg = MIMEMultipart("alternative")
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    if dry_run:
        log.info("[DRY RUN] Would send to %s — Subject: %s", to_address, subject)
        return True

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_address, msg.as_string())
        log.info("✅  Email sent to %s", to_address)
        return True
    except smtplib.SMTPAuthenticationError:
        log.error("❌  SMTP authentication failed. Check EMAIL_ADDRESS / EMAIL_PASSWORD in .env")
        return False
    except Exception as exc:
        log.error("❌  Failed to send email to %s: %s", to_address, exc)
        return False


# ── Core logic ─────────────────────────────────────────────────────────────────

def process_birthdays(contacts: list[dict], dry_run: bool = False) -> tuple[int, int]:
    """Check all contacts; send emails to those with birthdays today. Returns (sent, failed)."""
    today = date.today()
    sent, failed = 0, 0

    birthday_contacts = [c for c in contacts if is_birthday_today(c.get("dob", ""))]

    if not birthday_contacts:
        log.info("No birthdays today (%s). Nothing to send.", today.strftime("%B %d"))
        return 0, 0

    log.info("🎂  Found %d birthday(s) today!", len(birthday_contacts))

    for contact in birthday_contacts:
        name = contact.get("name", "Friend")
        email = contact.get("email", "")
        age = calculate_age(contact["dob"])

        if not email:
            log.warning("Skipping %s — no email address", name)
            failed += 1
            continue

        context = {
            "name": name,
            "age": age,
            "nickname": contact.get("nickname", name.split()[0]),
            "relationship": contact.get("relationship", "friend"),
            "sender_name": contact.get("sender_name", "Your Friend"),
            "extra_message": contact.get("extra_message", ""),
            "year": today.year,
        }

        subject = f"🎂 Happy Birthday, {context['nickname']}!"
        html_body = render_template("birthday.html", context)
        text_body = render_template("birthday.txt", context)

        success = send_email(email, subject, html_body, text_body, dry_run=dry_run)
        if success:
            sent += 1
        else:
            failed += 1

    return sent, failed


# ── CLI ────────────────────────────────────────────────────────────────────────

def cmd_list(contacts: list[dict]):
    """Print upcoming birthdays to the terminal."""
    upcoming = upcoming_birthdays(contacts, days=365)
    today = date.today()

    print(f"\n{'─'*58}")
    print(f"  🎂  Birthdays  (today: {today.strftime('%B %d, %Y')})")
    print(f"{'─'*58}")
    if not upcoming:
        print("  No contacts found.")
    for c in upcoming:
        days = c["_days_until"]
        label = "TODAY 🎉" if days == 0 else f"in {days} day{'s' if days != 1 else ''}"
        age = calculate_age(c["dob"])
        age_str = f"turns {age}" if age else ""
        print(f"  {c['name']:<22} {c['_next_bday'].strftime('%b %d')}  {age_str:<10}  {label}")
    print(f"{'─'*58}\n")


def cmd_test(contacts: list[dict]):
    """Send a test email to the sender's own address."""
    log.info("Sending test email to %s …", EMAIL_ADDRESS)
    context = {
        "name": "Test User",
        "age": 30,
        "nickname": "Test",
        "relationship": "friend",
        "sender_name": "Birthday Mailer Bot",
        "extra_message": "This is a test email — everything is working! 🎉",
        "year": date.today().year,
    }
    html_body = render_template("birthday.html", context)
    text_body = render_template("birthday.txt", context)
    send_email(EMAIL_ADDRESS, "🎂 Test Birthday Email", html_body, text_body)


def main():
    parser = argparse.ArgumentParser(description="Automated Birthday Email Sender")
    parser.add_argument("--dry-run", action="store_true", help="Preview emails without sending")
    parser.add_argument("--test", action="store_true", help="Send a test email to yourself")
    parser.add_argument("--list", action="store_true", help="List upcoming birthdays")
    args = parser.parse_args()

    contacts = load_contacts()

    if args.list:
        cmd_list(contacts)
    elif args.test:
        cmd_test(contacts)
    else:
        sent, failed = process_birthdays(contacts, dry_run=args.dry_run)
        log.info("Done. Sent: %d | Failed: %d", sent, failed)


if __name__ == "__main__":
    main()
