"""
Quick test: send an email via MailerSend SMTP using .env credentials.
  python scripts/send_test_email.py
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.mailersend.net")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
FROM_EMAIL = os.environ.get("MAIL_DEFAULT_SENDER", SMTP_USER)
FROM_NAME = os.environ.get("MAIL_DEFAULT_SENDER_NAME", "ICSE Accommodation Test")
TO_EMAIL = os.environ.get("MAIL_NOTIFY_TO", "gpinto@ufpa.br")


def main():
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "[ICSE Accommodation] SMTP test"
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = TO_EMAIL

    msg.attach(MIMEText("This is a plain-text test email sent via MailerSend SMTP.", "plain", "utf-8"))
    msg.attach(MIMEText("<p>This is an <strong>HTML test email</strong> sent via MailerSend SMTP.</p>", "html", "utf-8"))

    print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} (TLS)...")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
    print("Email sent successfully to", TO_EMAIL)


if __name__ == "__main__":
    main()
