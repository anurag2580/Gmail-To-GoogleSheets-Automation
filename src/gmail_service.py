import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import src.config as config

def get_gmail_service():
    """Authenticates and returns the Gmail service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', config.SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Point to the credentials folder
            creds_path = os.path.join(os.path.dirname(__file__), '../credentials/credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, config.SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def fetch_unread_emails(service):
    """Fetches list of unread emails from Inbox[cite: 31, 49]."""
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
    return results.get('messages', [])

def mark_as_read(service, msg_id):
    """Removes UNREAD label to prevent duplicate processing[cite: 32, 52]."""
    service.users().messages().modify(
        userId='me',
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()