import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

IMAP_HOST = os.getenv("IMAP_HOST")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

PHISHING_KEYWORDS = ["lottery", "prize", "account suspended", "verify your account", "password reset"]

def email_imap_reader(max_messages=30):
    """Fetch latest emails from inbox via IMAP with phishing check"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        email_list = []

        if status != "OK":
            return email_list

        msg_numbers = messages[0].split()[-max_messages:]

        for num in reversed(msg_numbers):
            status, msg_data = mail.fetch(num, "(RFC822)")
            if status != "OK":
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg.get("Subject"))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8", errors="ignore")
                    from_ = msg.get("From")
                    date_ = msg.get("Date")

                    status_text = "✅ Clean"
                    for kw in PHISHING_KEYWORDS:
                        if kw.lower() in (subject or "").lower():
                            status_text = "⚠️ Possible Phishing"
                            break

                    email_list.append({
                        "from": from_,
                        "subject": subject,
                        "date": date_,
                        "status": status_text
                    })
        mail.logout()
        return email_list

    except Exception as e:
        print("Error fetching emails:", e)
        return []

def scan_emails(max_messages=20):
    return email_imap_reader(max_messages=max_messages)
