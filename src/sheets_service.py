from googleapiclient.discovery import build

def get_sheets_service(creds):
    return build('sheets', 'v4', credentials=creds)

def append_row(service, spreadsheet_id, row):
    body = {
        'values': [[
            row['from'],
            row['subject'],
            row['date'],
            row['body']
        ]]
    }

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range='Sheet1!A:D',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
