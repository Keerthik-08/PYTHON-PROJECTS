# 🎂 Birthday Mailer

Automated birthday email sender. Store your friends & family's date of birth and
Birthday Mailer will send them a personalized HTML email every year — automatically.

---

## ✨ Features

- **Personalized HTML emails** with name, age, relationship, and a custom message
- **Plain-text fallback** for email clients that don't render HTML
- **Dry-run mode** — preview without sending a single email
- **Upcoming birthdays list** — see who's next in the next 30/365 days
- **Test mode** — fire a test email to yourself to verify everything works
- **Auto-scheduling** via cron (Linux/macOS) — set it once, forget it
- **VS Code launch configs** — run any mode with one click

---

## 🚀 Quick Start

### 1. Clone / open the project

```bash
cd birthday-mailer
code .          # open in VS Code
```

### 2. Create a virtual environment & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Or use the VS Code task: **Terminal → Run Task → Install Dependencies**

### 3. Configure credentials

```bash
cp .env.example .env
```

Open `.env` and fill in:

```env
EMAIL_ADDRESS=you@gmail.com
EMAIL_PASSWORD=xxxx-xxxx-xxxx-xxxx   # Gmail App Password
```

> **Gmail users**: You need an **App Password**, not your regular password.
> Enable 2-Step Verification, then go to:
> https://myaccount.google.com/apppasswords

### 4. Add your contacts

```bash
cp data/contacts.example.json data/contacts.json
```

Edit `data/contacts.json`:

```json
[
  {
    "name": "Alice Johnson",
    "nickname": "Ali",
    "email": "alice@example.com",
    "dob": "1992-05-23",
    "relationship": "best friend",
    "sender_name": "Your Name",
    "extra_message": "Remember our road trip? Here's to more adventures!"
  }
]
```

| Field | Required | Description |
|---|---|---|
| `name` | ✅ | Full name |
| `email` | ✅ | Recipient email |
| `dob` | ✅ | Date of birth `YYYY-MM-DD` |
| `nickname` | ❌ | Used in subject line (defaults to first name) |
| `relationship` | ❌ | e.g. mother, friend, colleague |
| `sender_name` | ❌ | Your name in the sign-off |
| `extra_message` | ❌ | Personal note appended to the email |

---

## 🖥️ Usage

```bash
# Send emails for today's birthdays
python birthday_mailer.py

# Preview without sending (safe to run any time)
python birthday_mailer.py --dry-run

# List all upcoming birthdays
python birthday_mailer.py --list

# Send a test email to yourself
python birthday_mailer.py --test
```

### VS Code Run Configs (F5)

| Config | Action |
|---|---|
| ▶ Run: Send Today's Birthdays | Send real emails |
| 🔍 Dry Run | Preview only |
| 📧 Send Test Email | Email to yourself |
| 📋 List Upcoming Birthdays | Terminal table |

---

## ⏰ Automatic Daily Scheduling

### Linux / macOS (cron)

Run the VS Code task **"Add Cron Job (Daily at 8 AM)"**, or manually:

```bash
crontab -e
```

Add this line (update the path):

```
0 8 * * * cd /path/to/birthday-mailer && .venv/bin/python birthday_mailer.py >> logs/cron.log 2>&1
```

### Windows (Task Scheduler)

1. Open **Task Scheduler** → Create Basic Task
2. Trigger: **Daily** at 8:00 AM
3. Action: **Start a program**
   - Program: `C:\path\to\.venv\Scripts\python.exe`
   - Arguments: `birthday_mailer.py`
   - Start in: `C:\path\to\birthday-mailer`

---

## 📁 Project Structure

```
birthday-mailer/
├── birthday_mailer.py      # Main script
├── config.py               # Loads .env settings
├── template_engine.py      # Jinja2 template renderer
├── requirements.txt
├── .env.example            # Copy → .env and fill in
├── .gitignore
│
├── data/
│   ├── contacts.json       # Your contacts (git-ignored)
│   └── contacts.example.json
│
├── templates/
│   ├── birthday.html       # Rich HTML email
│   └── birthday.txt        # Plain-text fallback
│
├── logs/                   # Auto-created on first run
│   └── birthday_mailer.log
│
└── .vscode/
    ├── launch.json         # Run configurations
    ├── tasks.json          # Setup & utility tasks
    ├── settings.json       # Editor settings
    └── extensions.json     # Recommended extensions
```

---

## 🔒 Security Notes

- `.env` and `data/contacts.json` are both **git-ignored** — they will never be committed
- Use an **App Password** for Gmail, not your real password
- Keep your `.env` file private

---

## 📧 Supported Email Providers

| Provider | SMTP Host | Port |
|---|---|---|
| Gmail | `smtp.gmail.com` | 587 |
| Outlook / Hotmail | `smtp-mail.outlook.com` | 587 |
| Yahoo | `smtp.mail.yahoo.com` | 587 |
| iCloud | `smtp.mail.me.com` | 587 |

Set `SMTP_HOST` and `SMTP_PORT` in your `.env` file.

---

## 📝 License

MIT — free to use and modify.
