# Scopes: Read/Modify Gmail (to mark as read), Read/Write Sheets
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Create a blank Google Sheet and paste its ID here
# URL format: docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
SPREADSHEET_ID = '1LYr0EfRj1YgU3_D3om74SuuawGuUwXg3A6qPmRMlqX8' 
RANGE_NAME = 'Sheet1!A:E' # Appending to columns A-E