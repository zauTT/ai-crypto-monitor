import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

CREDS_PATH = "crypto_creds.json"
Scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_ID = "1funEXQuIcJDERgZ31b16rIbWj32GB-wJwnyt0PojHVA"

def get_gspread_client():
    """Authorize Google SHeets client."""
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=Scopes)
    return gspread.authorize(creds)

def log_crypto_data(btc: float, eth: float, summary: str, sentiment: str):
    """Append crypto + AI summary +sentiment to Google Sheet."""
    client = get_gspread_client()

    spreadsheet = client.open_by_key(SHEET_ID)
    try:
        worksheet = spreadsheet.worksheet("AI_Crypto_Log")
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title="AI_Crypto_Log", rows="1000", cols="5")
        worksheet.append_row(["Timestamp", "BTC (USD)", "ETH (USD)", "Summary", "Sentiment"])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    worksheet.append_row([timestamp, btc, eth, summary, sentiment])
    print(f"✅ Logged to AI_Crypto_Log at {timestamp}")


