import os
from dotenv import load_dotenv
from gmail_service import connect_gmail, fetch_unseen_emails, mark_as_seen
from gemini_service import setup_gemini, summarize_email

load_dotenv()

# Your credentials
username = os.getenv("GMAIL_USER")
password = os.getenv("GMAIL_PASS")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def main():
    # Setup services
    mail = connect_gmail(username, password)
    model = setup_gemini(GEMINI_API_KEY)

    # Fetch emails
    emails = fetch_unseen_emails(mail, limit=5)

    if not emails:
        print("No unseen emails found.")
        return

    for email_data in emails:
        #result = summarize_email(model, email_data)

        print("=" * 70)
        print("FROM:", email_data["from"])
        print("SUBJECT:", email_data["subject"])
        #print("\n SUMMARY:")
        #print("Summary:", result["summary"])
        #print("Category:", result["category"])
        #print("Priority:", result["priority"])
        print("=" * 70)

        # Mark as seen
        mark_as_seen(mail, email_data["id"])

    mail.logout()


if __name__ == "__main__":
    main()
