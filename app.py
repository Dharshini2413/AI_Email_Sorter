import os
import streamlit as st
from dotenv import load_dotenv

from gmail_service import connect_gmail, fetch_unseen_emails, mark_as_seen
from gemini_service import setup_gemini, summarize_email

# Load env variables
load_dotenv()

USERNAME = os.getenv("GMAIL_USER")
PASSWORD = os.getenv("GMAIL_PASS")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="AI Email Summarizer", layout="wide")

st.title(" AI Gmail Summarizer")
st.write("Summarize and categorize your unread emails using Gemini")

if st.button("Fetch & Summarize Unread Emails"):

    with st.spinner("Connecting to Gmail..."):
        mail = connect_gmail(USERNAME, PASSWORD)

    with st.spinner("Setting up Gemini..."):
        model = setup_gemini(GEMINI_API_KEY)

    emails = fetch_unseen_emails(mail, limit=5)

    if not emails:
        st.success("No unread emails 🎉")
    else:
        categorized_emails = {}
        for email_data in emails:
            result = summarize_email(model, email_data)
            category = result["category"]

            if category not in categorized_emails:
                categorized_emails[category] = []

            categorized_emails[category].append({
            "subject": email_data["subject"],
            "from": email_data["from"],
            "summary": result["summary"],
            "priority": result["priority"]
             })
            mark_as_seen(mail, email_data["id"])

        st.markdown("##  Organized by Category")

        for category, items in categorized_emails.items():
            st.markdown(f"### 🏷 {category}")

        for item in items:
            with st.container():
                st.write("**Subject:**", item["subject"])
                st.write(" From:", item["from"])
                st.write(" Priority:", item["priority"])
                st.write(" Summary:", item["summary"])
                st.markdown("---")

            

    mail.logout()
