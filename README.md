# Gmail to Google Sheets Automation

## 1. High-Level Architecture Diagram
This project follows a clean, modular pipeline architecture where unread emails from Gmail are fetched, processed, and logged into Google Sheets securely.

### Architecture Overview:

- Gmail Inbox acts as the data source.
- Gmail API is used to fetch only unread emails.
- OAuth 2.0 handles secure authentication and authorization.
- A central Email Processing Engine parses and filters emails.
- Duplicate prevention is handled using Gmail labels.
- Google Sheets API appends structured data into a spreadsheet.

## 2. Step-by-Step Setup Instructions
- Clone the Repository
- Install Dependencies
  - pip install -r requirements.txt
- Google Cloud Configuration
  - Create a Google Cloud project.
  - Enable:
    - Gmail API
    - Google Sheets API
  - Configure OAuth Consent Screen (External).
  - Create OAuth Client ID (Desktop App).
  - Download credentials.json.
- Place the file here:
  - credentials/credentials.json
- Configure Script (Bonus)
  - In config.py, optionally enable subject filtering:
    - FILTER_SUBJECT = None "Process all unread emails"
    - FILTER_SUBJECT = "Invoice" "Bonus: only invoice emails"
- Run the Script
  - python src/main.py
## 3. Detailed Explanations
### OAuth Flow Used
The project uses OAuth 2.0 Desktop Application Flow.
### How it works:
- User authenticates via browser.
- Google issues an access token and refresh token.
- Tokens are stored locally in token.pickle.
- On subsequent runs, tokens are reused without re-login.
### Duplicate Prevention Logic
Duplicate emails are prevented using Gmail labels.
### Mechanism:
1. Script fetches only emails with: "Inbox + Unread"
2. After processing an email:
   - The UNREAD label is removed.
3. On re-run:
   - Gmail API no longer returns already processed emails.
## 4. State Persistence Method
State is maintained implicitly using two mechanisms:
### 1. OAuth Token Persistence
- Stored in token.pickle
- Avoids repeated authentication
### 2. Gmail Label State
- Processed emails are marked as READ
- Gmail itself acts as the state store
## Challenge Faced and Solution
### Challenge:
While integrating Google Sheets API, the script initially failed with a 403 insufficient authentication scopes error.
### Root Cause:
The OAuth token was generated earlier with Gmail-only permissions and did not include Sheets scope.
### Solution:
- Updated OAuth scopes to include Google Sheets.
- Deleted the old token.
- Re authenticated to generate a new token with correct scopes.
### Outcome:
- Sheets access worked correctly.
- Learned importance of scope-bound OAuth tokens.
## Limitations of the Solution
- Only processes emails from Gmail Inbox.
- Relies on Gmail labels for state (no database).
- Processes emails in batches to avoid long runs.
- Requires manual OAuth setup initially.
- Does not handle attachments.
## Bonus Features Implemented
- Subject-based filtering (configurable)
- Exclusion of automated no-reply emails
- HTML to plain-text email conversion
- Logging with timestamps
- Batch processing limit per run
