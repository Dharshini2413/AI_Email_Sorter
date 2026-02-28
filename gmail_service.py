import imaplib
import email
from email.header import decode_header


# Your credentials
username = "<your_email_id>"
password = "<your_app_password"


def connect_gmail(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail


def fetch_unseen_emails(mail, limit=5):
    status, messages = mail.search(None, "UNSEEN")
    mail_ids = messages[0].split()

    emails = []

    for i in mail_ids[-limit:]:
        status, msg_data = mail.fetch(i, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")

                from_ = msg.get("From")
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))

                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode(errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                emails.append({
                    "id": i,
                    "from": from_,
                    "subject": subject,
                    "body": body
                })

    return emails

def mark_as_seen(mail, email_id):
    mail.store(email_id, '+FLAGS', '\\Seen')
