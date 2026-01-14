import logging
from gmail_service import get_gmail_service
from email_parser import parse_email
from sheets_service import get_sheets_service, append_row
from config import FILTER_SUBJECT


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SPREADSHEET_ID = "1rFjztFsFwTdi9YPEfo-WwvwaR-mBH7nrC7oV7sPzMGI"

gmail_service, creds = get_gmail_service()

sheets_service = get_sheets_service(creds)

query = None
if FILTER_SUBJECT:
    query = f"subject:{FILTER_SUBJECT}"
    logging.info(f"Subject filter enabled: {FILTER_SUBJECT}")
else:
    logging.info("No subject filter enabled. Processing all unread emails.")

results = gmail_service.users().messages().list(
    userId='me',
    labelIds=['INBOX', 'UNREAD'],
    q=query
).execute()

messages = results.get('messages', [])
logging.info(f"Unread emails found: {len(messages)}")

MAX_EMAILS_PER_RUN = 10

for msg in messages[:MAX_EMAILS_PER_RUN]:
    data = parse_email(gmail_service, msg['id'])

    if not data:
        logging.info("Skipped automated email")
        continue

    append_row(sheets_service, SPREADSHEET_ID, data)
    logging.info("Email appended to sheet")

    gmail_service.users().messages().modify(
        userId='me',
        id=msg['id'],
        body={'removeLabelIds': ['UNREAD']}
    ).execute()

logging.info("Run completed successfully")
