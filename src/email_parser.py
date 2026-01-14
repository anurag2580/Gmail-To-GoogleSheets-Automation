import base64
from bs4 import BeautifulSoup

def parse_email(service, msg_id):
    """Extracts Sender, Subject, Date, Content, and Attachment Filenames."""
    msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
    payload = msg['payload']
    headers = payload.get('headers', [])

    email_data = {
        "From": "", 
        "Subject": "", 
        "Date": "", 
        "Content": "",
        "Attachments": "None" 
    }

    # 1. Parse Headers
    for h in headers:
        if h['name'] == 'From': email_data['From'] = h['value']
        if h['name'] == 'Subject': email_data['Subject'] = h['value']
        if h['name'] == 'Date': email_data['Date'] = h['value']

    # 2. Parse Body & Attachments
    parts = payload.get('parts', [])
    body_data = None
    attachment_files = []

    if not parts:
        # Simple email (no attachments, no HTML/Text split)
        body_data = payload.get('body', {}).get('data')
    else:
        for part in parts:
            # Check for File Name
            fname = part.get('filename')
            if fname:
                attachment_files.append(fname)
            
            # Look for Body content (Text/HTML)
            mimeType = part.get('mimeType')
            if mimeType == 'text/plain' and not body_data:
                body_data = part['body'].get('data')
            elif mimeType == 'text/html' and not body_data: # Fallback
                body_data = part['body'].get('data')
                
            # Handle nested multipart (sometimes text is deeper inside)
            if part.get('parts'):
                for subpart in part.get('parts'):
                    if subpart.get('mimeType') == 'text/plain' and not body_data:
                         body_data = subpart['body'].get('data')

    # 3. Format Data
    if attachment_files:
        email_data['Attachments'] = ", ".join(attachment_files)

    if body_data:
        try:
            text = base64.urlsafe_b64decode(body_data).decode('utf-8')
            email_data['Content'] = BeautifulSoup(text, "html.parser").get_text().strip()
        except Exception:
            email_data['Content'] = "(Error decoding body)"
    
    return email_data