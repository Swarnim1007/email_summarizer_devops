import imaplib
import email
from transformers import pipeline, AutoTokenizer
from app.models import db, Email
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the summarizer pipeline
summarizer = pipeline("summarization", model="knkarthick/MEETING_SUMMARY", tokenizer=AutoTokenizer.from_pretrained("knkarthick/MEETING_SUMMARY"))

def fetch_and_summarize_emails():
    # Create an IMAP4_SSL instance
    imap = imaplib.IMAP4_SSL("imap.gmail.com")

    # Login with your Gmail account credentials
    user_email = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_PASSWORD")
    imap.login(user_email, password)

    # Define the sender and date filters
    sender = "keshav agarwal"
    date = '12-Apr-2024'

    # Select the INBOX mailbox
    imap.select('"INBOX"')

    # Search for unread emails from the specified sender on the specified date
    status, messages = imap.search(None, f'ON "{date}"', f'FROM "{sender}"', 'all')

    # Iterate over the messages and retrieve their contents
    for num in messages[0].split():
        _, msg = imap.fetch(num, "(RFC822)")
        message = email.message_from_bytes(msg[0][1])

        # Extract the email content
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True)
                    body = content.decode("utf-8")
                    break
        else:
            if message.get_content_type() == "text/plain":
                content = message.get_payload(decode=True)
                body = content.decode("utf-8")
                break

        # Summarize the email content
        content_summarised = summarizer(body, max_length=100, min_length=10, truncation=True)[0]['summary_text']

        # Save the summarized email to the database and mark it as read
        email_entry = Email(sender=message["From"], subject=message['Subject'], body=body, summary=content_summarised, read=False)
        db.session.add(email_entry)
        db.session.commit()

    # Logout from the IMAP session
    imap.logout()
