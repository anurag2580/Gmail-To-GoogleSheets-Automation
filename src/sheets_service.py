import os.path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import src.config as config

def get_sheets_service():
    """Authenticating and returning the Sheets service."""
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', config.SCOPES)
        return build('sheets', 'v4', credentials=creds)
    else:
        raise Exception("No token found. Run Gmail auth first.")

def append_to_sheet(service, data):
    """Appending a row of data to the configured Google Sheet."""
    body = {'values': [data]}
    service.spreadsheets().values().append(
        spreadsheetId=config.SPREADSHEET_ID,
        range=config.RANGE_NAME,
        valueInputOption='RAW',
        body=body
    ).execute()