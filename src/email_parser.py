from bs4 import BeautifulSoup
import base64
from email.utils import parsedate_to_datetime

def parse_email(service, msg_id):
    msg = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()

    headers = msg['payload']['headers']
    payload = msg['payload']

    data = {
        "from": "",
        "subject": "",
        "date": "",
        "body": ""
    }

    for h in headers:
        if h['name'] == 'From':
            data['from'] = h['value']
        elif h['name'] == 'Subject':
            data['subject'] = h['value']
        elif h['name'] == 'Date':
            data['date'] = parsedate_to_datetime(h['value']).isoformat()

    # Exclude automated emails
    if 'no-reply' in data['from'].lower():
        return None

    raw_body = ""

    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('mimeType') in ['text/plain', 'text/html']:
                body = part['body'].get('data')
                if body:
                    raw_body = base64.urlsafe_b64decode(body).decode()
                    break
    else:
        body = payload['body'].get('data')
        if body:
            raw_body = base64.urlsafe_b64decode(body).decode()

    # CLEAN HTML → TEXT
    soup = BeautifulSoup(raw_body, "html.parser")
    data['body'] = soup.get_text(separator=" ", strip=True)

    return data
