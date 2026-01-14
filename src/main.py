import time
from datetime import datetime
from src.gmail_service import get_gmail_service, fetch_unread_emails, mark_as_read
from src.sheets_service import get_sheets_service, append_to_sheet
from src.email_parser import parse_email

def job():
    """The main task to run every cycle."""
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking for new emails...")
    
    # Authenticate (Token is cached, so this is fast)
    gmail = get_gmail_service()
    sheets = get_sheets_service()

    # Fetch
    messages = fetch_unread_emails(gmail)

    # Logic: You can add the "20 email" rule here if you really want, 
    # but it's better to process whatever you find immediately.
    if not messages:
        print(" -> No new emails.")
        return

    print(f" -> Found {len(messages)} unread emails. Processing...")

    for msg in messages:
        try:
            msg_id = msg['id']
            
            # Parse
            data = parse_email(gmail, msg_id)
            row = [
                data['From'],
                data['Subject'], 
                data['Date'], 
                data['Content'],
                data['Attachments']
                ]

            # Append to Sheets
            append_to_sheet(sheets, row)
            
            # Mark as Read (State Persistence)
            mark_as_read(gmail, msg_id)
            print(f"    -> Processed: {data['Subject'][:30]}...")

        except Exception as e:
            print(f"    -> Error processing {msg_id}: {e}")

def main():
    print("--- Gmail Automation Started (Press Ctrl+C to stop) ---")
    
    while True:
        try:
            job()
            # Wait for 60 seconds before checking again
            print("Sleeping for 60 seconds...\n")
            time.sleep(60) 
        except KeyboardInterrupt:
            print("Stopping automation...")
            break
        except Exception as e:
            print(f"Critical Error: {e}")
            time.sleep(60) # Wait before retrying

if __name__ == "__main__":
    main()