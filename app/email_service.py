"""
Email sending via MailerSend SMTP.
Reads configuration from environment variables:
  SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
  MAIL_DEFAULT_SENDER, MAIL_DEFAULT_SENDER_NAME
"""

import html
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Union

from flask import current_app


def send_mail(
    to: Union[str, List[str]],
    subject: str,
    body_text: str,
    body_html: str = None,
    reply_to: str = None,
) -> bool:
    """
    Send an email via MailerSend SMTP (STARTTLS on port 587).

    Args:
        to: recipient address(es).
        subject: email subject.
        body_text: plain-text body.
        body_html: HTML body (optional).
        reply_to: reply-to address (optional).

    Returns:
        True on success, False on failure.
    """
    if isinstance(to, str):
        to = [to]

    host = current_app.config.get("SMTP_HOST", "smtp.mailersend.net") if current_app else os.environ.get("SMTP_HOST", "smtp.mailersend.net")
    port = int(current_app.config.get("SMTP_PORT", 587) if current_app else os.environ.get("SMTP_PORT", 587))
    username = (current_app.config.get("SMTP_USERNAME") or "") if current_app else os.environ.get("SMTP_USERNAME", "")
    password = (current_app.config.get("SMTP_PASSWORD") or "") if current_app else os.environ.get("SMTP_PASSWORD", "")
    sender_email = current_app.config.get("MAIL_DEFAULT_SENDER", username) if current_app else os.environ.get("MAIL_DEFAULT_SENDER", username)
    sender_name = (current_app.config.get("MAIL_DEFAULT_SENDER_NAME") or "") if current_app else os.environ.get("MAIL_DEFAULT_SENDER_NAME", "")

    from_header = f"{sender_name} <{sender_email}>" if sender_name else sender_email

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_header
    msg["To"] = ", ".join(to)
    if reply_to:
        msg["Reply-To"] = reply_to

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    if body_html:
        msg.attach(MIMEText(body_html, "html", "utf-8"))

    try:
        with smtplib.SMTP(host, port, timeout=30) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(username, password)
            smtp.sendmail(sender_email, to, msg.as_string())
        return True
    except Exception as e:
        if current_app:
            current_app.logger.exception("Failed to send email: %s", e)
        return False


def send_new_accommodation_notification(entry) -> bool:
    """
    Send an informative email to MAIL_NOTIFY_TO when a new accommodation is registered.
    `entry` is an AccommodationRequest instance.
    """
    to = current_app.config.get("MAIL_NOTIFY_TO", "gpinto@ufpa.br")
    subject = f"[ICSE Accommodation] New registration: {entry.name}"

    def line(label, value):
        return f"{label}: {value}\n" if value is not None and value != "" else ""

    body_text = (
        "A new accommodation request was submitted.\n\n"
        + line("Name", entry.name)
        + line("Email", entry.email)
        + line("Institution", entry.institution)
        + line("Check-in", entry.check_in)
        + line("Check-out", entry.check_out)
        + line("Gender", entry.gender)
        + line("Roommate preference", entry.roommate_gender_pref)
        + line("Smoker", "Yes" if entry.smoker else "No")
        + line("Accepts smoker", "Yes" if entry.accepts_smoker else "No")
        + line("Social media", entry.social_media)
        + line("Website", entry.website)
        + line("Notes", entry.notes)
        + f"\nSubmitted at: {entry.created_at}"
    )

    def h(s):
        return html.escape(str(s)) if s is not None else ""

    body_html = (
        "<h2>New accommodation request</h2>"
        "<table border=\"1\" cellpadding=\"6\" cellspacing=\"0\" style=\"border-collapse: collapse;\">"
        f"<tr><td><b>Name</b></td><td>{h(entry.name)}</td></tr>"
        f"<tr><td><b>Email</b></td><td><a href=\"mailto:{entry.email}\">{h(entry.email)}</a></td></tr>"
        f"<tr><td><b>Institution</b></td><td>{h(entry.institution)}</td></tr>"
        f"<tr><td><b>Check-in</b></td><td>{entry.check_in}</td></tr>"
        f"<tr><td><b>Check-out</b></td><td>{entry.check_out}</td></tr>"
        f"<tr><td><b>Gender</b></td><td>{h(entry.gender)}</td></tr>"
        f"<tr><td><b>Roommate preference</b></td><td>{h(entry.roommate_gender_pref)}</td></tr>"
        f"<tr><td><b>Smoker</b></td><td>{'Yes' if entry.smoker else 'No'}</td></tr>"
        f"<tr><td><b>Accepts smoker</b></td><td>{'Yes' if entry.accepts_smoker else 'No'}</td></tr>"
    )
    if entry.social_media:
        body_html += f"<tr><td><b>Social media</b></td><td>{h(entry.social_media)}</td></tr>"
    if entry.website:
        body_html += f"<tr><td><b>Website</b></td><td><a href=\"{h(entry.website)}\">{h(entry.website)}</a></td></tr>"
    if entry.notes:
        body_html += f"<tr><td><b>Notes</b></td><td>{h(entry.notes)}</td></tr>"
    body_html += f"<tr><td><b>Submitted at</b></td><td>{entry.created_at}</td></tr></table>"

    return send_mail(to=to, subject=subject, body_text=body_text, body_html=body_html)
